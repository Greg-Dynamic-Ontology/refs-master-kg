"""IT-2R1S2 — Scenario: Preserve the direction of a projection.

IT-2R1 — Rule: A projects-to relationship identifies its source and target projections

Given a source projection
And a target projection
When the source projection projects to the target projection
Then the source projection is distinguishable from the target projection
And the projects-to relationship is directed from source to target.
"""

from machinery.src.projection import Projection, projects_to


def test_IT_2R1S2_preserve_direction_of_projection():
    source = Projection(identity="example-source-projection")
    target = Projection(identity="example-target-projection")

    forward = projects_to(source=source, target=target)
    reverse = projects_to(source=target, target=source)

    assert forward.source_projection != forward.target_projection, (
        "IT-2R1S2: The source and target projections must remain distinguishable."
    )
    assert (forward.source_projection, forward.target_projection) == (source, target), (
        "IT-2R1S2: The relationship must be directed from the supplied source to target."
    )
    assert (reverse.source_projection, reverse.target_projection) == (target, source), (
        "IT-2R1S2: Reversing the inputs must reverse the endpoint roles."
    )
    assert forward != reverse, (
        "IT-2R1S2: A source-to-target relationship must differ from its reverse."
    )