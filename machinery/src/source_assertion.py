"""Retain source and derived assertion identity, traceability, and location for IT-1R3 and IT-1R4."""

from dataclasses import dataclass, field

from machinery.src.source_identity import GovernedSourceIdentity


@dataclass(frozen=True)
class SourceAssertion:
    """An assertion recorded directly from a governed source artifact."""

    statement: str
    source_artifact: GovernedSourceIdentity | None = None
    source_location: str | None = None
    assertion_kind: str = field(default="source", init=False)


@dataclass(frozen=True)
class DerivedAssertion:
    """An assertion derived from one or more governed assertions."""

    statement: str
    derived_from: tuple[SourceAssertion, ...]
    assertion_kind: str = field(default="derived", init=False)


def record_source_assertion(
    *,
    statement: str,
    source_artifact: GovernedSourceIdentity,
    source_location: str | None = None,
) -> SourceAssertion:
    if isinstance(statement, DerivedAssertion):
        raise TypeError("A derived assertion cannot be recorded as a source assertion.")

    return SourceAssertion(
        statement=statement,
        source_artifact=source_artifact,
        source_location=source_location,
    )


def record_derived_assertion(
    *,
    statement: str,
    derived_from: tuple[SourceAssertion, ...],
) -> DerivedAssertion:
    return DerivedAssertion(
        statement=statement,
        derived_from=derived_from,
    )
