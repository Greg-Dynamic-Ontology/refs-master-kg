"""IT-1R2S2 — Scenario: Preserve the publisher boundary.

IT-1 — Feature: Govern source identity and provenance
IT-1R2 — Rule: A governed source artifact retains its provenance

Given governed source artifacts published by different authoritative organizations
When the artifacts are admitted as REFS source evidence
Then each artifact retains its publisher provenance
And equivalent content does not erase the publisher boundary.

Registration is the current in-memory admission operation. Equivalence is
supplied explicitly through a shared requirement, not inferred from identifiers.
"""

from machinery.src.gse_constraint import represent_gse_constraint
from machinery.src.source_artifact_registry import SourceArtifactRegistry
from machinery.src.source_identity import record_source_identity


def test_IT_1R2S2_preserve_publisher_boundary():
    # Synthetic identifiers deliberately coincide across governing organizations.
    fannie = record_source_identity(
        governing_source="Fannie Mae",
        source_provided_identity="example-constraint-001",
        publisher="Fannie Mae",
    )
    freddie = record_source_identity(
        governing_source="Freddie Mac",
        source_provided_identity="example-constraint-001",
        publisher="Freddie Mac",
    )
    shared = represent_gse_constraint(
        shared_requirement="Example requirement shared by both source constraints",
        source_constraints=(fannie, freddie),
    )
    registry = SourceArtifactRegistry()

    for source_artifact in shared.source_constraints:
        registry.register(source_artifact)

    assert len(registry.artifacts) == 2, (
        "IT-1R2S2: Equivalent content must not collapse two publishers' evidence."
    )
    assert {
        (artifact.governing_source, artifact.identity, artifact.publisher)
        for artifact in registry.artifacts
    } == {
        ("Fannie Mae", "example-constraint-001", "Fannie Mae"),
        ("Freddie Mac", "example-constraint-001", "Freddie Mac"),
    }, "IT-1R2S2: Each admitted artifact must retain its own publisher provenance."