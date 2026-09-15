"""Behavioral acceptance test for IT-1R2S1.

IT-1 — Feature: Govern source identity and provenance
IT-1R2 — Rule: A governed source artifact retains its provenance
IT-1R2S1 — Scenario: Identify the publisher of a governed source artifact

Given a source artifact with an explicitly supplied publisher,
when the artifact is recorded and registered,
then its publisher can be identified from the registered artifact.
"""

from machinery.src.source_artifact_registry import SourceArtifactRegistry
from machinery.src.source_identity import record_source_identity


def test_identify_publisher_of_governed_source_artifact():
    registry = SourceArtifactRegistry()
    artifact = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Artifact-00042",
        publisher="Example Publishing Organization",
    )

    registry.register(artifact)

    assert len(registry.artifacts) == 1
    assert registry.artifacts[0].publisher == "Example Publishing Organization"