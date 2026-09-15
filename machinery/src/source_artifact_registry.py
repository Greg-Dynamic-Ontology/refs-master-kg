"""Register and reprocess governed source artifacts for IT-1R1 and IT-1R5."""

from machinery.src.source_assertion import SourceAssertion
from machinery.src.source_identity import GovernedSourceIdentity


class SourceArtifactRegistry:
    def __init__(self):
        self.artifacts: list[GovernedSourceIdentity] = []
        self.source_assertions: list[SourceAssertion] = []

    def register(self, artifact: GovernedSourceIdentity) -> None:
        if artifact not in self.artifacts:
            self.artifacts.append(artifact)

    def reprocess(self, artifact: GovernedSourceIdentity) -> GovernedSourceIdentity:
        """Reuse the governed identity already registered for the same artifact."""
        for registered_artifact in self.artifacts:
            if registered_artifact == artifact:
                return registered_artifact

        self.register(artifact)
        return artifact

    def register_source_assertion(self, assertion: SourceAssertion) -> SourceAssertion:
        """Reuse an equivalent governed source assertion instead of duplicating it."""
        for registered_assertion in self.source_assertions:
            if registered_assertion == assertion:
                return registered_assertion

        self.source_assertions.append(assertion)
        return assertion