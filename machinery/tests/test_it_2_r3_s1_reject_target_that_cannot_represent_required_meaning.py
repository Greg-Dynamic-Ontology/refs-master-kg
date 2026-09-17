"""IT-2R3S1: Reject a target that cannot represent required meaning.

The RDF vocabulary and capability declarations below are synthetic test knowledge,
not declarations about a real serialization. They describe a complete capability
set for this request, including the selected mapping convention.
"""

from dataclasses import dataclass

import pytest
from rdflib import Graph, Namespace

from machinery.src.projection import Projection, projects_to


@dataclass(frozen=True)
class GovernedProjection(Projection):
    """Supply RDF projection knowledge to the existing projection entry point."""

    knowledge: Graph | None = None


def test_IT_2R3S1_reject_target_that_cannot_represent_required_meaning():
    terms = Namespace("urn:refs:test:IT-2R3S1:")
    knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R3S1:> .

        test:source
            test:containsMeaning test:qualifiedIdentity ;
            test:requiresMeaning test:qualifiedIdentity .

        test:target
            test:usesFormat test:limitedFormat ;
            test:usesConvention test:selectedConvention .

        test:limitedFormat
            test:capabilitiesComplete true ;
            test:supportsMeaning test:textValue .

        test:selectedConvention
            test:capabilitiesComplete true ;
            test:supportsMeaning test:textValue .
        ''',
        format="turtle",
    )
    source = GovernedProjection(
        identity=str(terms.source), governed_value="00042", knowledge=knowledge,
        capability_vocabulary=terms,
    )
    target = GovernedProjection(
        identity=str(terms.target), knowledge=knowledge, capability_vocabulary=terms
    )

    # The selected convention supplies no representation for qualifiedIdentity.
    # A copied lexical value alone cannot preserve that required meaning.
    try:
        projects_to(source=source, target=target)
    except ValueError as rejection:
        assert str(terms.qualifiedIdentity) in str(rejection), (
            "IT-2R3S1: Rejection must identify the required meaning that "
            f"cannot be represented: {terms.qualifiedIdentity}"
        )
    else:
        pytest.fail(
            "IT-2R3S1: Projection must be rejected when neither the target "
            "format nor the selected mapping convention can represent "
            f"required meaning: {terms.qualifiedIdentity}"
        )