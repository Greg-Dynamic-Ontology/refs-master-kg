"""IT-1R3S1 — Scenario: Trace a source assertion to its source artifact.

IT-1 — Feature: Govern source identity and provenance
IT-1R3 — Rule: Knowledge derived from a source artifact remains traceable
to that artifact

Given a registered source artifact containing an assertion
When REFS records that source assertion
Then the assertion retains a link to its source artifact
And the linked artifact's governed identity and publisher remain identifiable.

The assertion and source identifiers below are synthetic.
"""

from machinery.src.source_artifact_registry import SourceArtifactRegistry
from machinery.src.source_assertion import record_source_assertion
from machinery.src.source_identity import record_source_identity


def test_IT_1R3S1_trace_source_assertion_to_source_artifact():
    registry = SourceArtifactRegistry()
    artifact = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Publication-00042",
        publisher="Example Publishing Organization",
    )
    registry.register(artifact)

    assertion = record_source_assertion(
        statement="Example source assertion: an application includes a property address.",
        source_artifact=registry.artifacts[0],
    )

    assert assertion.statement == (
        "Example source assertion: an application includes a property address."
    ), "IT-1R3S1: The source assertion must retain its statement."

    assert assertion.source_artifact is not None, (
        "IT-1R3S1: The source assertion must retain a link to its source artifact."
    )

    linked_artifact = assertion.source_artifact
    assert (
        linked_artifact.governing_source,
        linked_artifact.identity,
        linked_artifact.publisher,
    ) == (
        "example-governing-source",
        "Publication-00042",
        "Example Publishing Organization",
    ), "IT-1R3S1: The assertion must trace to the correct source artifact and publisher."

    assert linked_artifact in registry.artifacts, (
        "IT-1R3S1: The linked source artifact must be identifiable in the registry."
    )