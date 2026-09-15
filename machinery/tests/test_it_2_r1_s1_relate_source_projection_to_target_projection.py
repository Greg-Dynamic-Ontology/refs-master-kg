"""IT-2R1S1 — Relate one source projection to one target projection.

IT-2R1 — Rule: A projects-to relationship identifies its source and target projections

Given a source projection
And a target projection
When the source projection projects to the target projection
Then the projects-to relationship identifies the source projection
And the projects-to relationship identifies the target projection.
"""

from machinery.src.projection import Projection, projects_to


def test_IT_2R1S1_relate_source_projection_to_target_projection():
    source = Projection(identity="example-source-projection")
    target = Projection(identity="example-target-projection")

    relationship = projects_to(source=source, target=target)

    assert (
        relationship.source_projection,
        relationship.target_projection,
    ) == (source, target), (
        "IT-2R1S1: The projects-to relationship must identify "
        "the supplied source projection and target projection."
    )