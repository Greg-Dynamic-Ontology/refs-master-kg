"""IT-2R2S1 — Scenario: Preserve a governed value across projections.

IT-2R2 — Rule: A projects-to relationship preserves required meaning

Given a source projection containing a governed value
When the source projection projects to a target projection
Then the target projection contains the governed value.
"""

from machinery.src.projection import Projection, projects_to


def test_IT_2R2S1_preserve_governed_value_across_projections():
    # Synthetic string value; its leading zeros are part of the value.
    source = Projection(
        identity="example-source-projection",
        governed_value="00042",
    )
    target = Projection(identity="example-target-projection")

    relationship = projects_to(source=source, target=target)

    assert relationship.target_projection is not None, (
        "IT-2R2S1: The relationship must identify the resulting target projection."
    )
    assert relationship.target_projection.governed_value == "00042", (
        "IT-2R2S1: The target projection must contain the governed value from the source."
    )