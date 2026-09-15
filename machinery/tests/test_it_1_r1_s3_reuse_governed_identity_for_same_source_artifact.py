"""Behavioral acceptance test for IT-1R1S3.

IT-1 — Feature: Govern source identity and provenance
IT-1R1 — Rule: Governed source identity is preserved when provided
by the governing source
IT-1R1S3 — Scenario: Reuse the governed identity for the same source artifact

Given a source artifact is already registered,
when it is encountered again with the same governing source and provided identity,
then its governed identity is reused without adding a duplicate registry entry.
"""

from machinery.src.source_artifact_registry import SourceArtifactRegistry
from machinery.src.source_identity import record_source_identity


def test_reuse_governed_identity_for_same_source_artifact():
    registry = SourceArtifactRegistry()
    original_artifact = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Artifact-00042",
    )
    registry.register(original_artifact)

    # A separate record represents encountering the same source artifact again.
    encountered_again = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Artifact-00042",
    )
    registry.register(encountered_again)

    assert [
        (registered.governing_source, registered.identity)
        for registered in registry.artifacts
    ] == [("example-governing-source", "Artifact-00042")]