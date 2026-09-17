"""IT-2R5S1: Equivalent governed results using distinct projection engines.

Proposed engine interface: PythonProjectionEngine and SparqlProjectionEngine
execute RDF rules using Python traversal and SPARQL respectively. They are real
implementations, not test doubles or aliases of the same execution path.
projects_to accepts the selected engine through its engine keyword argument.
"""

from rdflib import Graph, Literal, Namespace
from rdflib.compare import isomorphic
from rdflib.namespace import PROV, RDF

from machinery.src import projection


def test_IT_2R5S1_produce_equivalent_governed_results_using_different_projection_engines():
    terms = Namespace("urn:refs:test:IT-2R5S1:")
    source_knowledge = Graph().parse(data='''
        @prefix test: <urn:refs:test:IT-2R5S1:> .
        test:source a test:ResidentialMortgage ;
            test:identifier "00042" ;
            test:requiresMeaning test:identifier, test:classification .
        ''', format="turtle")
    target_knowledge = Graph().parse(data='''
        @prefix test: <urn:refs:test:IT-2R5S1:> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

        test:target test:usesFormat test:rdfFormat ;
            test:usesConvention test:convention ;
            test:usesPreferences test:preferences ;
            test:usesExpectations test:expectations .
        test:expectations test:requiresMeaning test:identifier, test:classification .
        test:rdfFormat test:capabilitiesComplete true ;
            test:supportsMeaning test:identifier, test:classification .
        test:convention test:capabilitiesComplete true ;
            test:supportsMeaning test:identifier, test:classification ;
            test:hasMapping test:identifierMapping ;
            test:hasDerivationRule test:mortgageIsLoan, test:disabledRule .
        test:identifierMapping test:sourcePredicate test:identifier ;
            test:targetPredicate test:identifier .
        test:preferences test:enablesRule test:mortgageIsLoan .
        test:mortgageIsLoan a test:DerivationRule ;
            test:premisePredicate rdf:type ;
            test:premiseObject test:ResidentialMortgage ;
            test:conclusionPredicate rdf:type ;
            test:conclusionObject test:Loan .
        test:disabledRule a test:DerivationRule ;
            test:premisePredicate rdf:type ;
            test:premiseObject test:ResidentialMortgage ;
            test:conclusionPredicate rdf:type ;
            test:conclusionObject test:UnselectedClassification .
        ''', format="turtle")
    source = projection.Projection(
        identity=str(terms.source), knowledge=source_knowledge,
        capability_vocabulary=terms,
    )
    target = projection.Projection(
        identity=str(terms.target), knowledge=target_knowledge,
        capability_vocabulary=terms,
    )
    original_source, original_target = set(source_knowledge), set(target_knowledge)

    engine_types = [
        getattr(projection, name, None)
        for name in ("PythonProjectionEngine", "SparqlProjectionEngine")
    ]
    assert all(callable(engine_type) for engine_type in engine_types), (
        "IT-2R5S1: Python and SPARQL projection engines must be available "
        "to execute the same governed mapping knowledge."
    )
    assert engine_types[0] is not engine_types[1], (
        "IT-2R5S1: The engines must be distinct implementations."
    )
    results = []
    for engine_type in engine_types:
        label = engine_type.__name__
        relationship = projection.projects_to(
            source=source, target=target, engine=engine_type()
        )
        assert relationship.target_projection is not None, f"IT-2R5S1: {label} must produce a target."
        result = relationship.target_projection.knowledge
        assert isinstance(result, Graph), f"IT-2R5S1: {label} must produce RDF knowledge."
        assert set(result.objects(terms.target, terms.identifier)) == {Literal("00042")}, (
            f"IT-2R5S1: {label} must preserve the identifier, including leading zeros."
        )
        assert (terms.target, RDF.type, terms.Loan) in result, (
            f"IT-2R5S1: {label} must apply the enabled derivation rule."
        )
        assert (terms.target, RDF.type, terms.UnselectedClassification) not in result, (
            f"IT-2R5S1: {label} must respect the selected preferences."
        )
        records = {
            record for record in result.subjects(RDF.type, terms.DerivedAssertion)
            if (record, RDF.subject, terms.target) in result
            and (record, RDF.predicate, RDF.type) in result
            and (record, RDF.object, terms.Loan) in result
            and (record, PROV.wasDerivedFrom, terms.source) in result
        }
        assert any(
            (activity, PROV.used, terms.mortgageIsLoan) in result
            and (activity, PROV.used, terms.preferences) in result
            for record in records
            for activity in result.objects(record, PROV.wasGeneratedBy)
        ), f"IT-2R5S1: {label} must retain derivation provenance."
        assert set(source_knowledge) == original_source and set(target_knowledge) == original_target, (
            f"IT-2R5S1: {label} must not alter the inputs used by the other engine."
        )
        results.append(result)

    # This fixture has no engine-specific metadata. Blank node names may differ.
    assert isomorphic(results[0], results[1]), (
        "IT-2R5S1: The engines must produce equivalent RDF knowledge, "
        "independently of serialization order and blank-node identifiers."
    )
