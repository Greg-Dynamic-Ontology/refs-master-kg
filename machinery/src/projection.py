"""Identify projection endpoints and enforce declared target capabilities."""

from dataclasses import dataclass, replace

from rdflib import BNode, Dataset, Graph, Literal, Namespace, URIRef
from rdflib.namespace import PROV, RDF
from rdflib.plugins.sparql.processor import SPARQLProcessor, SPARQLResult


@dataclass(frozen=True)
class Projection:
    identity: str
    governed_value: str | None = None
    knowledge: Graph | None = None
    capability_vocabulary: Namespace | None = None


@dataclass(frozen=True)
class ProjectsTo:
    source_projection: Projection | None = None
    target_projection: Projection | None = None
    projection_record: Graph | None = None


def _check_target_capabilities(
    source: Projection, target: Projection
) -> tuple[Graph, Namespace] | None:
    """Evaluate explicit, complete capability declarations in supplied RDF.

    The caller supplies the vocabulary namespace. Meaning identifiers, formats,
    conventions, and their capabilities are all read from the knowledge graph.
    Absence of a capability is decisive only for explicitly complete declarations.
    """
    graphs = [p.knowledge for p in (source, target) if p.knowledge is not None]
    if not graphs:
        return

    vocabularies = {
        str(p.capability_vocabulary)
        for p in (source, target)
        if p.capability_vocabulary is not None
    }
    if len(vocabularies) != 1:
        raise ValueError("Projection knowledge requires one explicit capability vocabulary.")
    vocabulary = Namespace(vocabularies.pop())
    knowledge = Graph()
    for graph in graphs:
        # Dataset governance declarations reside in its default graph.
        # Do not flatten named graphs or feed dataset quads to Graph.add().
        declarations = graph.default_graph if isinstance(graph, Dataset) else graph
        for triple in declarations:
            knowledge.add(triple)

    source_id = URIRef(source.identity)
    required = set(knowledge.objects(source_id, vocabulary.requiresMeaning))
    required_graphs = set(knowledge.objects(source_id, vocabulary.requiresNamedGraph))
    if required_graphs:
        required.add(vocabulary.namedGraphDistinctions)
    if not required:
        return knowledge, vocabulary

    target_id = URIRef(target.identity)
    formats = set(knowledge.objects(target_id, vocabulary.usesFormat))
    conventions = set(knowledge.objects(target_id, vocabulary.usesConvention))
    providers = formats | conventions
    if not formats or not conventions or any(
        (provider, vocabulary.capabilitiesComplete, Literal(True)) not in knowledge
        for provider in providers
    ):
        raise ValueError("Target capability evaluation requires complete format and convention declarations.")

    supported = {
        meaning
        for provider in providers
        for meaning in knowledge.objects(provider, vocabulary.supportsMeaning)
    }
    unsupported = required - supported
    if unsupported:
        identifiers = ", ".join(sorted(str(meaning) for meaning in unsupported))
        graph_details = ""
        if vocabulary.namedGraphDistinctions in unsupported and required_graphs:
            graph_names = ", ".join(sorted(str(graph_id) for graph_id in required_graphs))
            graph_details = f"; required named graph distinctions: {graph_names}"
        raise ValueError(
            f"Target {target.identity} cannot represent required meaning: "
            f"{identifiers}{graph_details}"
        )

    return knowledge, vocabulary


def _apply_mapping_conventions(
    source: Projection, target: Projection, knowledge: Graph, vocabulary: Namespace
) -> Graph:
    """Apply selected RDF predicate mappings without changing the input graphs.

    Mapping declarations supply predicates; RDF objects retain their original
    identity, datatype, language, and lexical content. Only source assertions
    about the source projection are mapped by this operation.
    """
    result = Graph()
    if target.knowledge is not None:
        for prefix, namespace in target.knowledge.namespaces():
            result.bind(prefix, namespace)
        for triple in target.knowledge:
            result.add(triple)

    source_id = URIRef(source.identity)
    target_id = URIRef(target.identity)
    for convention in knowledge.objects(target_id, vocabulary.usesConvention):
        applied = False
        for mapping in knowledge.objects(convention, vocabulary.hasMapping):
            source_predicates = set(knowledge.objects(mapping, vocabulary.sourcePredicate))
            target_predicates = set(knowledge.objects(mapping, vocabulary.targetPredicate))
            if (
                len(source_predicates) != 1
                or len(target_predicates) != 1
                or not all(isinstance(p, URIRef) for p in source_predicates | target_predicates)
            ):
                raise ValueError(
                    f"Mapping {mapping} requires one source predicate and one target predicate IRI."
                )
            source_predicate = next(iter(source_predicates))
            target_predicate = next(iter(target_predicates))
            if source.knowledge is None:
                continue
            for value in source.knowledge.objects(source_id, source_predicate):
                result.add((target_id, target_predicate, value))
                applied = True
            # Retain the declared mapping needed to interpret the result.
            for triple in knowledge.triples((mapping, None, None)):
                result.add(triple)
        if applied:
            result.add((target_id, vocabulary.appliedConvention, convention))
            result.add((target_id, vocabulary.usesConvention, convention))
            for triple in knowledge.triples((convention, None, None)):
                result.add(triple)
    return result


def _apply_assertion_rules(
    source: Projection,
    target: Projection,
    knowledge: Graph,
    vocabulary: Namespace,
    result: Graph,
    *,
    rule_link: URIRef,
    rule_type: URIRef,
    assertion_type: URIRef,
) -> None:
    """Apply selected single-premise rules and record assertion-level provenance.

    A rule matches a predicate/object assertion about the source projection and
    declares a predicate/object conclusion about the target. Rule content is RDF
    knowledge, not domain-specific Python logic. Only rules enabled by selected
    preferences and belonging to a selected convention are evaluated.
    """
    if source.knowledge is None:
        return
    source_facts = (
        source.knowledge.default_graph
        if isinstance(source.knowledge, Dataset)
        else source.knowledge
    )
    source_id = URIRef(source.identity)
    target_id = URIRef(target.identity)
    preferences = set(knowledge.objects(target_id, vocabulary.usesPreferences))
    for convention in knowledge.objects(target_id, vocabulary.usesConvention):
        for rule in knowledge.objects(convention, rule_link):
            enabling_preferences = {
                preference for preference in preferences
                if (preference, vocabulary.enablesRule, rule) in knowledge
            }
            if not enabling_preferences:
                continue
            if (rule, RDF.type, rule_type) not in knowledge:
                raise ValueError(f"Selected rule {rule} must be declared as {rule_type}.")

            fields = (
                vocabulary.premisePredicate,
                vocabulary.premiseObject,
                vocabulary.conclusionPredicate,
                vocabulary.conclusionObject,
            )
            values = []
            for field in fields:
                declared = set(knowledge.objects(rule, field))
                if len(declared) != 1:
                    raise ValueError(f"Rule {rule} requires exactly one {field}.")
                values.append(next(iter(declared)))
            premise_predicate, premise_object, conclusion_predicate, conclusion_object = values
            if not isinstance(premise_predicate, URIRef) or not isinstance(
                conclusion_predicate, URIRef
            ):
                raise ValueError(f"Rule {rule} predicates must be IRIs.")
            if (source_id, premise_predicate, premise_object) not in source_facts:
                continue

            result.add((target_id, conclusion_predicate, conclusion_object))
            assertion = BNode()
            activity = BNode()
            result.add((assertion, RDF.type, RDF.Statement))
            result.add((assertion, RDF.type, assertion_type))
            result.add((assertion, RDF.subject, target_id))
            result.add((assertion, RDF.predicate, conclusion_predicate))
            result.add((assertion, RDF.object, conclusion_object))
            result.add((assertion, PROV.wasDerivedFrom, source_id))
            result.add((assertion, PROV.wasGeneratedBy, activity))
            result.add((activity, RDF.type, PROV.Activity))
            result.add((activity, PROV.used, source_id))
            result.add((activity, PROV.used, rule))
            for preference in enabling_preferences:
                result.add((activity, PROV.used, preference))
            result.add((target_id, vocabulary.appliedConvention, convention))
            # Keep the actual rule and preferences available for interpretation.
            for resource in {rule, convention, *enabling_preferences}:
                for triple in knowledge.triples((resource, None, None)):
                    result.add(triple)


def _record_permitted_omissions(
    source: Projection,
    target: Projection,
    knowledge: Graph,
    vocabulary: Namespace,
    result: Graph,
) -> Graph:
    """Keep permitted, actual omissions in a separate REFS governance graph.

    This handles meaning identified by source predicates, as declared by the
    supplied expectations. Permission alone does not establish an omission.
    """
    record = Graph()
    if source.knowledge is None:
        return record
    source_facts = (
        source.knowledge.default_graph
        if isinstance(source.knowledge, Dataset)
        else source.knowledge
    )
    source_id, target_id = URIRef(source.identity), URIRef(target.identity)
    expectations = set(knowledge.objects(target_id, vocabulary.usesExpectations))
    required = set(knowledge.objects(source_id, vocabulary.requiresMeaning))
    for expectation in expectations:
        required.update(knowledge.objects(expectation, vocabulary.requiresMeaning))

    for expectation in expectations:
        for meaning in knowledge.objects(expectation, vocabulary.permitsOmission):
            if not isinstance(meaning, URIRef):
                raise ValueError("An omitted source predicate must be an IRI.")
            if meaning in required:
                raise ValueError(f"Omission permission conflicts with required meaning: {meaning}")
            if (expectation, vocabulary.nonRequiredMeaning, meaning) not in knowledge:
                raise ValueError(f"Omission requires explicit non-required status: {meaning}")

            # Account for both direct preservation and selected predicate mappings.
            target_predicates = {meaning}
            for convention in knowledge.objects(target_id, vocabulary.usesConvention):
                for mapping in knowledge.objects(convention, vocabulary.hasMapping):
                    if (mapping, vocabulary.sourcePredicate, meaning) in knowledge:
                        target_predicates.update(
                            knowledge.objects(mapping, vocabulary.targetPredicate)
                        )
            for value in source_facts.objects(source_id, meaning):
                if any((target_id, predicate, value) in result for predicate in target_predicates):
                    continue
                # An explicitly recorded transformation is not an omission.
                transformed = False
                for assertion in result.subjects(RDF.type, vocabulary.TransformedAssertion):
                    for activity in result.objects(assertion, PROV.wasGeneratedBy):
                        for rule in result.objects(activity, PROV.used):
                            if (
                                (rule, vocabulary.premisePredicate, meaning) in knowledge
                                and (rule, vocabulary.premiseObject, value) in knowledge
                                and (activity, PROV.used, source_id) in result
                            ):
                                transformed = True
                if transformed:
                    continue

                omission = BNode()
                record.add((omission, RDF.type, vocabulary.PermittedOmission))
                record.add((omission, RDF.type, RDF.Statement))
                record.add((omission, vocabulary.omittedMeaning, meaning))
                record.add((omission, vocabulary.targetProjection, target_id))
                record.add((omission, RDF.subject, source_id))
                record.add((omission, RDF.predicate, meaning))
                record.add((omission, RDF.object, value))
                record.add((omission, PROV.wasDerivedFrom, source_id))
                record.add((omission, vocabulary.permittedBy, expectation))
                for triple in knowledge.triples((expectation, None, None)):
                    record.add(triple)
    return record


class PythonProjectionEngine:
    """Execute governed mappings and rules through Python RDF traversal."""

    def project(self, source, target, knowledge, vocabulary):
        result = _apply_mapping_conventions(source, target, knowledge, vocabulary)
        for link, rule_type, assertion_type in (
            (vocabulary.hasDerivationRule, vocabulary.DerivationRule, vocabulary.DerivedAssertion),
            (vocabulary.hasTransformationRule, vocabulary.TransformationRule,
             vocabulary.TransformedAssertion),
        ):
            _apply_assertion_rules(
                source, target, knowledge, vocabulary, result,
                rule_link=link, rule_type=rule_type, assertion_type=assertion_type,
            )
        return result


class SparqlProjectionEngine:
    """Match governed mappings and rule premises with local SPARQL queries.

    Source evidence and rule knowledge occupy separate query graphs. This engine
    does not call the Python mapping or inference implementation. Capabilities
    and omission governance remain shared checks outside either engine.
    """

    def project(self, source, target, knowledge, vocabulary):
        result = Graph()
        if target.knowledge is not None:
            for prefix, namespace in target.knowledge.namespaces():
                result.bind(prefix, namespace)
            for triple in target.knowledge:
                result.add(triple)

        query_data = Dataset()
        rules_id = URIRef("urn:refs:engine:query:rules")
        facts_id = URIRef("urn:refs:engine:query:source")
        for triple in knowledge:
            query_data.graph(rules_id).add(triple)
        if source.knowledge is not None:
            facts = (
                source.knowledge.default_graph
                if isinstance(source.knowledge, Dataset) else source.knowledge
            )
            for triple in facts:
                query_data.graph(facts_id).add(triple)

        source_id, target_id = URIRef(source.identity), URIRef(target.identity)
        bindings = {
            "rules": rules_id, "facts": facts_id,
            "source": source_id, "target": target_id,
        }
        namespaces = {"v": vocabulary, "rdf": RDF}

        processor = SPARQLProcessor(query_data)

        def query(text, *, initBindings, initNs):
            # Dataset.query() in the installed RDFLib accesses the deprecated
            # default_context while dispatching to this same processor.
            return SPARQLResult(
                processor.query(text, initBindings=initBindings, initNs=initNs)
            )

        # Validate selected declarations even when they have no matching facts.
        mappings = query('''
            SELECT DISTINCT ?convention ?mapping WHERE {
                GRAPH ?rules {
                    ?target v:usesConvention ?convention .
                    ?convention v:hasMapping ?mapping .
                }
            }
        ''', initBindings=bindings, initNs=namespaces)
        for row in mappings:
            for field in (vocabulary.sourcePredicate, vocabulary.targetPredicate):
                values = set(knowledge.objects(row.mapping, field))
                if len(values) != 1 or not isinstance(next(iter(values)), URIRef):
                    raise ValueError(f"Mapping {row.mapping} requires one predicate IRI for {field}.")
            if source.knowledge is not None:
                for triple in knowledge.triples((row.mapping, None, None)):
                    result.add(triple)

        mapped = query('''
            SELECT DISTINCT ?convention ?outputPredicate ?value WHERE {
                GRAPH ?rules {
                    ?target v:usesConvention ?convention .
                    ?convention v:hasMapping ?mapping .
                    ?mapping v:sourcePredicate ?inputPredicate ;
                             v:targetPredicate ?outputPredicate .
                }
                GRAPH ?facts { ?source ?inputPredicate ?value . }
            }
        ''', initBindings=bindings, initNs=namespaces)
        for row in mapped:
            result.add((target_id, row.outputPredicate, row.value))
            result.add((target_id, vocabulary.appliedConvention, row.convention))
            result.add((target_id, vocabulary.usesConvention, row.convention))
            for triple in knowledge.triples((row.convention, None, None)):
                result.add(triple)

        if source.knowledge is None:
            return result
        for link, rule_type, assertion_type in (
            (vocabulary.hasDerivationRule, vocabulary.DerivationRule, vocabulary.DerivedAssertion),
            (vocabulary.hasTransformationRule, vocabulary.TransformationRule,
             vocabulary.TransformedAssertion),
        ):
            rule_bindings = {**bindings, "ruleLink": link}
            selected = query('''
                SELECT DISTINCT ?rule WHERE {
                    GRAPH ?rules {
                        ?target v:usesConvention ?convention ; v:usesPreferences ?preference .
                        ?convention ?ruleLink ?rule .
                        ?preference v:enablesRule ?rule .
                    }
                }
            ''', initBindings=rule_bindings, initNs=namespaces)
            for row in selected:
                if (row.rule, RDF.type, rule_type) not in knowledge:
                    raise ValueError(f"Selected rule {row.rule} must be declared as {rule_type}.")
                for field in (vocabulary.premisePredicate, vocabulary.premiseObject,
                              vocabulary.conclusionPredicate, vocabulary.conclusionObject):
                    values = set(knowledge.objects(row.rule, field))
                    if len(values) != 1:
                        raise ValueError(f"Rule {row.rule} requires exactly one {field}.")
                    if field in (vocabulary.premisePredicate, vocabulary.conclusionPredicate):
                        if not isinstance(next(iter(values)), URIRef):
                            raise ValueError(f"Rule {row.rule} predicates must be IRIs.")

            matches = query('''
                SELECT DISTINCT ?convention ?rule ?preference ?predicate ?object WHERE {
                    GRAPH ?rules {
                        ?target v:usesConvention ?convention ; v:usesPreferences ?preference .
                        ?convention ?ruleLink ?rule .
                        ?preference v:enablesRule ?rule .
                        ?rule v:premisePredicate ?inputPredicate ;
                              v:premiseObject ?inputObject ;
                              v:conclusionPredicate ?predicate ;
                              v:conclusionObject ?object .
                    }
                    GRAPH ?facts { ?source ?inputPredicate ?inputObject . }
                }
            ''', initBindings=rule_bindings, initNs=namespaces)
            grouped = {}
            for row in matches:
                key = (row.convention, row.rule, row.predicate, row.object)
                grouped.setdefault(key, set()).add(row.preference)
            for (convention, rule, predicate, value), preferences in grouped.items():
                result.add((target_id, predicate, value))
                assertion, activity = BNode(), BNode()
                for triple in (
                    (assertion, RDF.type, RDF.Statement),
                    (assertion, RDF.type, assertion_type),
                    (assertion, RDF.subject, target_id),
                    (assertion, RDF.predicate, predicate),
                    (assertion, RDF.object, value),
                    (assertion, PROV.wasDerivedFrom, source_id),
                    (assertion, PROV.wasGeneratedBy, activity),
                    (activity, RDF.type, PROV.Activity),
                    (activity, PROV.used, source_id),
                    (activity, PROV.used, rule),
                    (target_id, vocabulary.appliedConvention, convention),
                ):
                    result.add(triple)
                for preference in preferences:
                    result.add((activity, PROV.used, preference))
                for resource in {rule, convention, *preferences}:
                    for triple in knowledge.triples((resource, None, None)):
                        result.add(triple)
        return result


def projects_to(
    *, source: Projection, target: Projection,
    engine: PythonProjectionEngine | SparqlProjectionEngine | None = None,
) -> ProjectsTo:
    checked = _check_target_capabilities(source, target)
    projected_knowledge = target.knowledge
    projection_record = Graph()
    if checked is not None:
        knowledge, vocabulary = checked
        selected_engine = engine if engine is not None else PythonProjectionEngine()
        projected_knowledge = selected_engine.project(
            source, target, knowledge, vocabulary
        )
        projection_record = _record_permitted_omissions(
            source, target, knowledge, vocabulary, projected_knowledge
        )
    projected_target = replace(
        target, governed_value=source.governed_value, knowledge=projected_knowledge
    )
    return ProjectsTo(
        source_projection=source,
        target_projection=projected_target,
        projection_record=projection_record,
    )
