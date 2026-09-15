"""Retain source assertion traceability and location for IT-1R3S1 and IT-1R3S2."""

from dataclasses import dataclass

from machinery.src.source_identity import GovernedSourceIdentity


@dataclass(frozen=True)
class SourceAssertion:
    """An assertion recorded from a source, rather than a REFS inference."""

    statement: str
    source_artifact: GovernedSourceIdentity | None = None
    source_location: str | None = None


def record_source_assertion(
    *,
    statement: str,
    source_artifact: GovernedSourceIdentity,
    source_location: str | None = None,
) -> SourceAssertion:
    return SourceAssertion(
        statement=statement,
        source_artifact=source_artifact,
        source_location=source_location,
    )