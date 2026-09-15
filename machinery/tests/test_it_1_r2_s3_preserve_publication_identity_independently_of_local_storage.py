"""IT-1R2S3 — Preserve publication identity independently of local storage.

IT-1 — Feature: Govern source identity and provenance
IT-1R2 — Rule: A governed source artifact retains its provenance

Given a publication with a source-provided identity and a local storage path
When the same publication is recorded at another local storage path
Then each record retains its local path separately
And both records retain the same governed publication identity.

Paths and publication identifiers are synthetic; this test moves no files.
"""

from machinery.src.source_identity import record_source_identity


def test_IT_1R2S3_preserve_publication_identity_independently_of_local_storage():
    original = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Publication-00042",
        publisher="Example Publishing Organization",
        local_storage_path="C:/refs/downloads/publication.pdf",
    )

    relocated = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Publication-00042",
        publisher="Example Publishing Organization",
        local_storage_path="D:/refs/archive/renamed-publication.pdf",
    )

    assert (original.local_storage_path, relocated.local_storage_path) == (
        "C:/refs/downloads/publication.pdf",
        "D:/refs/archive/renamed-publication.pdf",
    ), (
        "IT-1R2S3: Local storage paths must be recorded separately "
        "from publication identity."
    )

    for record in (original, relocated):
        assert (record.governing_source, record.identity) == (
            "example-governing-source", "Publication-00042"
        ), (
            "IT-1R2S3: Local storage must not replace "
            "the source-provided publication identity."
        )

    assert original == relocated, (
        "IT-1R2S3: Different local paths must not create "
        "different governed identities."
    )