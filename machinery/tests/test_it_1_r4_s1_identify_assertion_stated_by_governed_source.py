"""IT-1R4S1 — Scenario: Identify an assertion stated by a governed source.

IT-1 — Feature: Govern source identity and provenance
IT-1R4 — Rule: Source assertions remain distinguishable from derived assertions

Given an assertion extracted directly from a governed source artifact
When the assertion is represented as REFS knowledge
Then it is identifiable as a source assertion.

All example source details are synthetic.
"""

from machinery.src.source_assertion import record_source_assertion
from machinery.src.source_identity import record_source_identity


def test_IT_1R4S1_identify_assertion_stated_by_governed_source():
    artifact = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Publication-00042",
        publisher="Example Publishing Organization",
    )

    assertion = record_source_assertion(
        statement="Example source assertion: an application includes a property address.",
        source_artifact=artifact,
    )

    assert getattr(assertion, "assertion_kind", None) == "source", (
        "IT-1R4S1: An assertion stated directly by a governed source "
        "must be identifiable as a source assertion."
    )