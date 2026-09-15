"""IT-1R2S1 — Scenario: Preserve the publisher boundary.

IT-1 — Feature: Govern source identity and provenance
IT-1R2 — Rule: A governed source artifact retains its provenance

Given Fannie Mae publishes a constraint
And Freddie Mac publishes an equivalent constraint
When REFS represents their shared requirement as a GSE constraint
Then the Fannie Mae source constraint remains identifiable
And the Freddie Mac source constraint remains identifiable
And the GSE constraint retains a link to each source constraint.
"""

from machinery.src.gse_constraint import represent_gse_constraint
from machinery.src.source_identity import record_source_identity


def test_IT_1R2S1_preserve_publisher_boundary():
    # Synthetic constraint IDs; equivalence is supplied, not inferred here.
    fannie_constraint = record_source_identity(
        governing_source="Fannie Mae",
        source_provided_identity="example-fannie-constraint-001",
        publisher="Fannie Mae",
    )
    freddie_constraint = record_source_identity(
        governing_source="Freddie Mac",
        source_provided_identity="example-freddie-constraint-001",
        publisher="Freddie Mac",
    )

    gse_constraint = represent_gse_constraint(
        shared_requirement="Example requirement shared by both source constraints",
        source_constraints=(fannie_constraint, freddie_constraint),
    )

    linked_sources = {
        (source.governing_source, source.identity, source.publisher)
        for source in gse_constraint.source_constraints
    }
    assert linked_sources == {
        ("Fannie Mae", "example-fannie-constraint-001", "Fannie Mae"),
        ("Freddie Mac", "example-freddie-constraint-001", "Freddie Mac"),
    }, (
        "IT-1R2S1: The GSE constraint must retain links "
        "to both publishers' source constraints."
    )