"""IT-2R6S2: Reject a target that violates its governed expectations.

External Turtle fixtures contain a target missing its required identifier and
the SHACL expectations it violates. Successful rejection makes this test PASS.
"""

from pathlib import Path

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, SH

from machinery.src.projection import Projection, evaluate_projection


def test_IT_2R6S2_reject_target_that_violates_governed_expectations():
    terms = Namespace("urn:refs:test:IT-2R6S2:")
    fixtures = Path(__file__).resolve().parent / "fixtures" / "uad"
    target_file = fixtures / "data-test-it2r6s2-target.ttl"
    expectations_file = fixtures / "data-test-it2r6s2-expectations.ttl"
    for fixture in (target_file, expectations_file):
        assert fixture.is_file(), f"IT-2R6S2: Missing fixture: {fixture}"
    knowledge = Graph().parse(target_file, format="turtle")
    expectations = Graph().parse(expectations_file, format="turtle")
    original_target, original_expectations = set(knowledge), set(expectations)
    target = Projection(identity=str(terms.target), knowledge=knowledge)

    assessment = evaluate_projection(target=target, expectations=expectations)

    assert assessment.accepted is False, (
        "IT-2R6S2: The evaluator must reject the target missing its required identifier."
    )
    report = assessment.validation_report
    assert isinstance(report, Graph), "IT-2R6S2: Rejection must include an RDF report."
    reports = set(report.subjects(RDF.type, SH.ValidationReport))
    assert len(reports) == 1, "IT-2R6S2: One report must describe the assessment."
    report_node = next(iter(reports))
    assert set(report.objects(report_node, SH.conforms)) == {Literal(False)}, (
        "IT-2R6S2: The report must explicitly state nonconformance."
    )
    failures = set(report.objects(report_node, SH.result))
    assert failures, "IT-2R6S2: Rejection must identify the violated expectation."
    assert any(
        (failure, RDF.type, SH.ValidationResult) in report
        and (failure, SH.focusNode, terms.target) in report
        and (failure, SH.sourceShape, terms.IdentifierExpectation) in report
        and (failure, SH.resultPath, terms.identifier) in report
        and (failure, SH.sourceConstraintComponent, SH.MinCountConstraintComponent) in report
        for failure in failures
    ), (
        "IT-2R6S2: The report must identify the target, identifier expectation, "
        "identifier path, and violated minimum-count constraint."
    )
    assert all(
        (failure, SH.sourceShape, terms.ClassificationExpectation) not in report
        for failure in failures
    ), "IT-2R6S2: The satisfied classification expectation must not be reported as violated."
    assert set(knowledge) == original_target, "IT-2R6S2: Evaluation must not alter the target."
    assert set(expectations) == original_expectations, (
        "IT-2R6S2: Evaluation must not alter the governed expectations."
    )
