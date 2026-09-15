"""Register governed source artifacts for IT-1R1S2 and IT-1R1S3."""

from machinery.src.source_identity import GovernedSourceIdentity


class SourceArtifactRegistry:
    def __init__(self):
        self.artifacts: list[GovernedSourceIdentity] = []

    def register(self, artifact: GovernedSourceIdentity) -> None:
        if artifact not in self.artifacts:
            self.artifacts.append(artifact)