"""Behavioral acceptance test for IT-1R1S2.

IT-1 — Feature: Govern source identity and provenance
IT-1R1 — Rule: Governed source identity is preserved when provided
by the governing source
IT-1R1S2 — Scenario: Register one governed source artifact

Given an empty registry and one artifact with a source-provided identity,
when the artifact is registered,
then the registry contains exactly that artifact with its identity preserved.
"""

from machinery.src.source_artifact_registry import SourceArtifactRegistry
from machinery.src.source_identity import record_source_identity


def test_register_one_governed_source_artifact():
    registry = SourceArtifactRegistry()
    artifact = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Artifact-00042",
    )

    registry.register(artifact)

    assert [
        (registered.governing_source, registered.identity)
        for registered in registry.artifacts
    ] == [("example-governing-source", "Artifact-00042")]