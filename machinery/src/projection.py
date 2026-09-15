"""Identify source and target projections for IT-2R1S1."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Projection:
    identity: str


@dataclass(frozen=True)
class ProjectsTo:
    source_projection: Projection | None = None
    target_projection: Projection | None = None


def projects_to(*, source: Projection, target: Projection) -> ProjectsTo:
    return ProjectsTo(source_projection=source, target_projection=target)