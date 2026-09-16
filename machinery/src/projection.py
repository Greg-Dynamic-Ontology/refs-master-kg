"""Identify projection endpoints and preserve governed values."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Projection:
    identity: str
    governed_value: str | None = None


@dataclass(frozen=True)
class ProjectsTo:
    source_projection: Projection | None = None
    target_projection: Projection | None = None


def projects_to(*, source: Projection, target: Projection) -> ProjectsTo:
    projected_target = replace(target, governed_value=source.governed_value)
    return ProjectsTo(source_projection=source, target_projection=projected_target)