"""Preserve source-constraint links across the publisher boundary for IT-1R2S1."""

from dataclasses import dataclass

from machinery.src.source_identity import GovernedSourceIdentity


@dataclass(frozen=True)
class GSEConstraint:
    shared_requirement: str
    source_constraints: tuple[GovernedSourceIdentity, ...] = ()


def represent_gse_constraint(
    *,
    shared_requirement: str,
    source_constraints: tuple[GovernedSourceIdentity, ...],
) -> GSEConstraint:
    """Represent a supplied shared requirement; equivalence is established upstream."""
    return GSEConstraint(
        shared_requirement=shared_requirement,
        source_constraints=source_constraints,
    )