"""Behavioral acceptance test for IT-1R1S4.

IT-1 — Feature: Govern source identity and provenance
IT-1R1 — Rule: Governed source identity is preserved when provided
by the governing source
IT-1R1S4 — Scenario: Distinguish different governed source artifacts

Given two artifacts with different governing-source/identity pairs,
when both are registered,
then both remain separately represented with their identities preserved.
"""

import pytest

from machinery.src.source_artifact_registry import SourceArtifactRegistry
from machinery.src.source_identity import record_source_identity


@pytest.mark.parametrize(
    "second_source, second_identity",
    [
        pytest.param(
            "example-source-A", "Artifact-00043", id="different-identities"
        ),
        pytest.param(
            "example-source-B", "Artifact-00042", id="different-governing-sources"
        ),
    ],
)
def test_distinguish_different_governed_source_artifacts(
    second_source, second_identity
):
    registry = SourceArtifactRegistry()
    first_artifact = record_source_identity(
        governing_source="example-source-A",
        source_provided_identity="Artifact-00042",
    )
    second_artifact = record_source_identity(
        governing_source=second_source,
        source_provided_identity=second_identity,
    )

    registry.register(first_artifact)
    registry.register(second_artifact)

    recorded = [
        (artifact.governing_source, artifact.identity)
        for artifact in registry.artifacts
    ]
    assert len(recorded) == 2
    assert set(recorded) == {
        ("example-source-A", "Artifact-00042"),
        (second_source, second_identity),
    }