"""Source identity recording for IT-1R1S1."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GovernedSourceIdentity:
    """An identity supplied by, and retained with, its governing source."""

    governing_source: str
    identity: str


def record_source_identity(
    *, governing_source: str, source_provided_identity: str
) -> GovernedSourceIdentity:
    """Preserve a provided identity verbatim, without minting or normalizing it.

    This scenario covers provided identities only. Missing-identity policy
    and persistent storage are outside this operation's scope.
    """
    return GovernedSourceIdentity(
        governing_source=governing_source,
        identity=source_provided_identity,
    )