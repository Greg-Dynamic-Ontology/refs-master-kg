"""Source identity and publisher recording for IT-1R1S1 and IT-1R2S1."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GovernedSourceIdentity:
    """An identity supplied by, and retained with, its governing source."""

    governing_source: str
    identity: str
    # Publisher is provenance, not part of the governed identity comparison.
    publisher: str | None = field(default=None, compare=False)
    # Local storage locates a copy; it does not define publication identity.
    local_storage_path: str | None = field(default=None, compare=False)


def record_source_identity(
    *,
    governing_source: str,
    source_provided_identity: str,
    publisher: str | None = None,
    local_storage_path: str | None = None,
) -> GovernedSourceIdentity:
    """Preserve a provided identity verbatim, without minting or normalizing it.

    This scenario covers provided identities only. Missing-identity policy
    and persistent storage are outside this operation's scope.
    """
    return GovernedSourceIdentity(
        governing_source=governing_source,
        identity=source_provided_identity,
        publisher=publisher,
        local_storage_path=local_storage_path,
    )