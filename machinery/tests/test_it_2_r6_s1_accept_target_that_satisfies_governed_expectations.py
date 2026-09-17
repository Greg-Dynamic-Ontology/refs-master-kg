"""IT-2R6S1: Accept a target satisfying its governed expectations.

Expectations are SHACL RDF knowledge. This tests evaluation of an existing
target, not generation of that target. Proposed interface:
evaluate_projection(target=..., expectations=...) returns an assessment with
accepted and validation_report attributes.
"""

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, SH

from machinery.src import projection


def test_IT_2R6S1_accept_target_that_satisfies_governed_expectations():
    terms = Namespace("urn:refs:test:IT-2R6S1:")
    target_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R6S1:> .
        test:target a test:Loan ; test:identifier "00042" .
        ''',
        format="turtle",
    )
    expectations = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R6S1:> .
        @prefix sh: <http://www.w3.org/ns/shacl#> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        test:TargetExpectations a sh:NodeShape ;
            sh:targetNode test:target ;
            sh:property test:IdentifierExpectation, test:ClassificationExpectation .

        test:IdentifierExpectation a sh:PropertyShape ;
            sh:path test:identifier ;
            sh:minCount 1 ;
            sh:maxCount 1 ;
            sh:datatype xsd:string ;
            sh:hasValue "00042" .

        test:ClassificationExpectation a sh:PropertyShape ;
            sh:path rdf:type ;
            sh:hasValue test:Loan .
        ''',
        format="turtle",
    )
    target = projection.Projection(identity=str(terms.target), knowledge=target_knowledge)
    original_target = set(target_knowledge)
    original_expectations = set(expectations)

    evaluate = getattr(projection, "evaluate_projection", None)
    assert callable(evaluate), (
        "IT-2R6S1: A projection evaluator must be available to test the target "
        "against its governed RDF expectations."
    )
    assessment = evaluate(target=target, expectations=expectations)

    assert assessment.accepted is True, (
        "IT-2R6S1: The assessment must accept a target that satisfies its "
        "governed expectations."
    )
    report = assessment.validation_report
    assert isinstance(report, Graph), (
        "IT-2R6S1: The assessment must provide an RDF validation report."
    )
    reports = set(report.subjects(RDF.type, SH.ValidationReport))
    assert len(reports) == 1, "IT-2R6S1: One validation report must describe the assessment."
    report_node = next(iter(reports))
    assert set(report.objects(report_node, SH.conforms)) == {Literal(True)}, (
        "IT-2R6S1: The validation report must confirm conformance."
    )
    assert not list(report.objects(report_node, SH.result)), (
        "IT-2R6S1: This fully conforming fixture must have no validation failures."
    )
    assert set(target_knowledge) == original_target, (
        "IT-2R6S1: Evaluation must not change the target being assessed."
    )
    assert set(expectations) == original_expectations, (
        "IT-2R6S1: Evaluation must not change its governed expectations."
    )
    """IT-2R6S1: Accept a target satisfying its governed expectations.

Expectations are SHACL RDF knowledge. This tests evaluation of an existing
target, not generation of that target. Proposed interface:
evaluate_projection(target=..., expectations=...) returns an assessment with
accepted and validation_report attributes.
"""

from pathlib import Path

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, SH

from machinery.src import projection


def test_IT_2R6S1_accept_target_that_satisfies_governed_expectations():
    terms = Namespace("urn:refs:test:IT-2R6S1:")
    fixtures = Path(__file__).resolve().parent / "fixtures" / "uad"
    target_file = fixtures / "data-test-it2r6s1-target.ttl"
    expectations_file = fixtures / "data-test-it2r6s1-expectations.ttl"
    for fixture in (target_file, expectations_file):
        assert fixture.is_file(), f"IT-2R6S1: Missing fixture: {fixture}"
    target_knowledge = Graph().parse(target_file, format="turtle")
    expectations = Graph().parse(expectations_file, format="turtle")
    target = projection.Projection(identity=str(terms.target), knowledge=target_knowledge)
    original_target = set(target_knowledge)
    original_expectations = set(expectations)

    evaluate = getattr(projection, "evaluate_projection", None)
    assert callable(evaluate), (
        "IT-2R6S1: A projection evaluator must be available to test the target "
        "against its governed RDF expectations."
    )
    assessment = evaluate(target=target, expectations=expectations)

    assert assessment.accepted is True, (
        "IT-2R6S1: The assessment must accept a target that satisfies its "
        "governed expectations."
    )
    report = assessment.validation_report
    assert isinstance(report, Graph), (
        "IT-2R6S1: The assessment must provide an RDF validation report."
    )
    reports = set(report.subjects(RDF.type, SH.ValidationReport))
    assert len(reports) == 1, "IT-2R6S1: One validation report must describe the assessment."
    report_node = next(iter(reports))
    assert set(report.objects(report_node, SH.conforms)) == {Literal(True)}, (
        "IT-2R6S1: The validation report must confirm conformance."
    )
    assert not list(report.objects(report_node, SH.result)), (
        "IT-2R6S1: This fully conforming fixture must have no validation failures."
    )
    assert set(target_knowledge) == original_target, (
        "IT-2R6S1: Evaluation must not change the target being assessed."
    )
    assert set(expectations) == original_expectations, (
        "IT-2R6S1: Evaluation must not change its governed expectations."
    )

