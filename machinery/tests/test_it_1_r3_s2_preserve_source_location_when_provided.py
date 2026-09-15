"""IT-1R3S2 — Scenario: Preserve source location when the source provides one.

IT-1 — Feature: Govern source identity and provenance
IT-1R3 — Rule: Knowledge derived from a source artifact remains traceable
to that artifact

Given a source artifact provides a location for an assertion
When REFS records the source assertion
Then the source-provided location is preserved exactly
And it remains associated with the assertion's source artifact.

The location is within the publication, not a local storage path.
All example source details are synthetic.
"""

from machinery.src.source_assertion import record_source_assertion
from machinery.src.source_identity import record_source_identity


def test_IT_1R3S2_preserve_source_location_when_provided():
    artifact = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Publication-00042",
        publisher="Example Publishing Organization",
        local_storage_path="C:/refs/downloads/publication.pdf",
    )

    assertion = record_source_assertion(
        statement="Example source assertion: an application includes a property address.",
        source_artifact=artifact,
        source_location="Section 03.2(a), paragraph 04",
    )

    assert assertion.source_location == "Section 03.2(a), paragraph 04", (
        "IT-1R3S2: The assertion must preserve the source-provided location exactly."
    )
    assert assertion.source_artifact == artifact, (
        "IT-1R3S2: The location must remain associated with the correct source artifact."
    )