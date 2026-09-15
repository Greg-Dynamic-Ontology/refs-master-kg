"""IT-1R3S3 — Trace independently published assertions independently.

IT-1 — Feature: Govern source identity and provenance
IT-1R3 — Rule: Knowledge derived from a source artifact remains traceable
to that artifact

Given two publishers' source artifacts contain the same assertion statement
When REFS records both source assertions
Then the assertions remain distinct
And each traces to its own source artifact, publisher, and source location.

All publication identifiers, locations, and assertion content are synthetic.
"""

from machinery.src.source_assertion import record_source_assertion
from machinery.src.source_identity import record_source_identity


def test_IT_1R3S3_trace_independently_published_assertions_independently():
    fannie_artifact = record_source_identity(
        governing_source="Fannie Mae",
        source_provided_identity="example-publication-001",
        publisher="Fannie Mae",
    )
    freddie_artifact = record_source_identity(
        governing_source="Freddie Mac",
        source_provided_identity="example-publication-001",
        publisher="Freddie Mac",
    )
    statement = "Example source assertion: an application includes a property address."

    fannie_assertion = record_source_assertion(
        statement=statement,
        source_artifact=fannie_artifact,
        source_location="Example section A.01",
    )
    freddie_assertion = record_source_assertion(
        statement=statement,
        source_artifact=freddie_artifact,
        source_location="Example section B.02",
    )

    assert fannie_assertion.statement == freddie_assertion.statement == statement, (
        "IT-1R3S3: Both source assertions must retain the supplied statement."
    )
    assert fannie_assertion != freddie_assertion, (
        "IT-1R3S3: Identical statements from different sources must remain distinct."
    )

    for assertion, expected in (
        (fannie_assertion, (
            "Fannie Mae", "example-publication-001", "Fannie Mae", "Example section A.01"
        )),
        (freddie_assertion, (
            "Freddie Mac", "example-publication-001", "Freddie Mac", "Example section B.02"
        )),
    ):
        assert assertion.source_artifact is not None, (
            "IT-1R3S3: Each assertion must retain its source-artifact link."
        )
        source = assertion.source_artifact
        assert (
            source.governing_source,
            source.identity,
            source.publisher,
            assertion.source_location,
        ) == expected, (
            "IT-1R3S3: Each assertion must trace independently to its own "
            "source artifact, publisher, and location."
        )