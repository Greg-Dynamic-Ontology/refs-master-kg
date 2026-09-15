"""Behavioral acceptance test for IT-1R5S1.

IT-1 — Feature: Govern source identity and provenance
IT-1R5 — Rule: Reprocessing governed source evidence preserves identity
IT-1R5S1 — Scenario: Reprocess a governed source artifact

Given a governed source artifact already represented as REFS source evidence,
when the artifact is processed again,
then its governed identity remains unchanged.
"""

from machinery.src.source_artifact_registry import SourceArtifactRegistry
from machinery.src.source_identity import record_source_identity


def test_reprocess_governed_source_artifact_preserves_identity():
    registry = SourceArtifactRegistry()

    original_artifact = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Artifact-00042",
    )
    registry.register(original_artifact)

    reprocessed_artifact = registry.reprocess(original_artifact)

    assert reprocessed_artifact is original_artifact
    assert reprocessed_artifact.identity == "Artifact-00042"