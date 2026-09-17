"""Identify projection endpoints and enforce declared target capabilities."""

from dataclasses import dataclass, replace

from rdflib import Dataset, Graph, Literal, Namespace, URIRef


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


def projects_to(*, source: Projection, target: Projection) -> ProjectsTo:
    checked = _check_target_capabilities(source, target)
    projected_knowledge = target.knowledge
    if checked is not None:
        knowledge, vocabulary = checked
        projected_knowledge = _apply_mapping_conventions(source, target, knowledge, vocabulary)
    projected_target = replace(
        target, governed_value=source.governed_value, knowledge=projected_knowledge
    )
    return ProjectsTo(source_projection=source, target_projection=projected_target)
