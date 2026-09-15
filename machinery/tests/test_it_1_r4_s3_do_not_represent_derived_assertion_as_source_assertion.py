"""IT-1R4S3 — Scenario: Do not represent a derived assertion as a source assertion.

IT-1 — Feature: Govern source identity and provenance
IT-1R4 — Rule: Source assertions remain distinguishable from derived assertions

Given an assertion not explicitly stated by a governed source artifact
When the assertion is derived during knowledge construction
Then the derived assertion cannot be represented as a source assertion.

All example source details are synthetic.
"""

import pytest

from machinery.src.source_assertion import (
    record_derived_assertion,
    record_source_assertion,
)
from machinery.src.source_identity import record_source_identity


def test_IT_1R4S3_do_not_represent_derived_assertion_as_source_assertion():
    artifact = record_source_identity(
        governing_source="example-governing-source",
        source_provided_identity="Publication-00042",
        publisher="Example Publishing Organization",
    )

    governed_assertion = record_source_assertion(
        statement="Example assertion explicitly stated by the governed source.",
        source_artifact=artifact,
    )

    derived_assertion = record_derived_assertion(
        statement="Example assertion derived during knowledge construction.",
        derived_from=(governed_assertion,),
    )

    with pytest.raises(TypeError, match="derived assertion"):
        record_source_assertion(
            statement=derived_assertion,
            source_artifact=artifact,
        )