"""IT-1R4S2 — Scenario: Identify an assertion derived from governed knowledge.

IT-1 — Feature: Govern source identity and provenance
IT-1R4 — Rule: Source assertions remain distinguishishable from derived assertions

Given an assertion derived from one or more governed assertions
When the derived assertion is represented as REFS knowledge
Then it is identifiable as a derived assertion
And its derivation is traceable to the governed assertions used to derive it.

All example source details are synthetic.
"""

import machinery.src.source_assertion as source_assertion
from machinery.src.source_identity import record_source_identity


def test_IT_1R4S2_identify_assertion_derived_from_governed_knowledge():
    first_artifact = record_source_identity(
        governing_source="example-governing-source-a",
        source_provided_identity="Publication-00042",
        publisher="Example Publishing Organization A",
    )
    second_artifact = record_source_identity(
        governing_source="example-governing-source-b",
        source_provided_identity="Publication-00084",
        publisher="Example Publishing Organization B",
    )

    first_assertion = source_assertion.record_source_assertion(
        statement="Example governed assertion A.",
        source_artifact=first_artifact,
    )
    second_assertion = source_assertion.record_source_assertion(
        statement="Example governed assertion B.",
        source_artifact=second_artifact,
    )

    record_derived_assertion = getattr(
        source_assertion,
        "record_derived_assertion",
        None,
    )

    assert callable(record_derived_assertion), (
        "IT-1R4S2: REFS must provide a way to represent an assertion "
        "derived from governed knowledge."
    )

    derived_assertion = record_derived_assertion(
        statement="Example assertion derived from governed knowledge.",
        derived_from=(first_assertion, second_assertion),
    )

    assert getattr(derived_assertion, "assertion_kind", None) == "derived", (
        "IT-1R4S2: An assertion derived from governed knowledge must be "
        "identifiable as a derived assertion."
    )

    assert getattr(derived_assertion, "derived_from", None) == (
        first_assertion,
        second_assertion,
    ), (
        "IT-1R4S2: A derived assertion must remain traceable to the governed "
        "assertions used to derive it."
    )