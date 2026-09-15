"""Behavioral acceptance test for IT-1R1S1.

IT-1 — Feature: Govern source identity and provenance
IT-1R1 — Rule: Governed source identity is preserved when provided
by the governing source
IT-1R1S1 — Scenario: Preserve a source-provided identity

Given a governing source provides an identity,
when REFS records the governed source identity,
then the source-provided identity is preserved.
"""

import pytest

from machinery.src.source_identity import record_source_identity


# Synthetic identifiers, not actual MISMO identifiers.
@pytest.mark.parametrize(
    "supplied_identity",
    [
        pytest.param("Source-00042", id="mixed-case"),
        pytest.param("source-00042", id="lowercase"),
        pytest.param("00042", id="leading-zeros"),
        pytest.param(
            "urn:example:Source/A#01",
            id="uri-punctuation-and-case",
        ),
    ],
)
def test_preserve_source_provided_identity(supplied_identity):
    recorded = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity=supplied_identity,
    )

    assert recorded.identity == supplied_identity
    assert recorded.governing_source == "example-governing-source"