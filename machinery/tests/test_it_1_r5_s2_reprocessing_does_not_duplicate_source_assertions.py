"""Behavioral acceptance test for IT-1R5S2.

IT-1 — Feature: Govern source identity and provenance
IT-1R5 — Rule: Reprocessing governed source evidence preserves identity
IT-1R5S2 — Scenario: Reprocessing does not duplicate source assertions

Given assertions already extracted from a governed source artifact,
when the same artifact is processed again without source changes,
then equivalent source assertions retain their governed identities
and duplicate source assertions are not created.

All example source details are synthetic.
"""

import pytest

from machinery.src.source_artifact_registry import SourceArtifactRegistry
from machinery.src.source_assertion import record_source_assertion
from machinery.src.source_identity import record_source_identity


def test_IT_1R5S2_reprocessing_does_not_duplicate_source_assertions():
    registry = SourceArtifactRegistry()
    artifact = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Publication-00042",
        publisher="Example Publishing Organization",
    )
    registry.register(artifact)

    original_assertion = record_source_assertion(
        statement="Example source assertion: an application includes a property address.",
        source_artifact=artifact,
        source_location="Section 03.2(a), paragraph 04",
    )
    reprocessed_assertion = record_source_assertion(
        statement="Example source assertion: an application includes a property address.",
        source_artifact=registry.reprocess(artifact),
        source_location="Section 03.2(a), paragraph 04",
    )

    register_source_assertion = getattr(
        registry,
        "register_source_assertion",
        None,
    )
    if not callable(register_source_assertion):
        pytest.fail(
            "IT-1R5S2: REFS must register source assertions so equivalent "
            "assertions can retain identity during reprocessing."
        )

    registered_original = register_source_assertion(original_assertion)
    registered_reprocessed = register_source_assertion(reprocessed_assertion)

    assert registered_reprocessed is registered_original, (
        "IT-1R5S2: Reprocessing unchanged source evidence must reuse the "
        "existing governed source assertion identity."
    )
    assert len(registry.source_assertions) == 1, (
        "IT-1R5S2: Reprocessing unchanged source evidence must not create "
        "a duplicate source assertion."
    )