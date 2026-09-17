"""IT-2R3S2: Preserve a concept through an explicit mapping convention.

Synthetic RDF knowledge describes the mapping and the target capabilities.
The full identity must survive; copying the local value alone is insufficient.
"""

from rdflib import Graph, Literal, Namespace

from machinery.src.projection import Projection, projects_to


def test_IT_2R3S2_preserve_concept_through_explicit_mapping_convention():
    terms = Namespace("urn:refs:test:IT-2R3S2:")
    source_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R3S2:> .

        test:source
            test:containsMeaning test:qualifiedIdentity ;
            test:requiresMeaning test:qualifiedIdentity ;
            test:qualifiedIdentity "urn:example:publisher-a:00042" .
        ''',
        format="turtle",
    )
    target_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R3S2:> .

        test:target
            test:usesFormat test:textOnlyFormat ;
            test:usesConvention test:identityAsText .

        test:textOnlyFormat
            test:capabilitiesComplete true ;
            test:supportsMeaning test:textValue .

        test:identityAsText
            test:capabilitiesComplete true ;
            test:supportsMeaning test:qualifiedIdentity ;
            test:hasMapping test:identityMapping .

        test:identityMapping
            test:sourcePredicate test:qualifiedIdentity ;
            test:targetPredicate test:identityText .
        ''',
        format="turtle",
    )
    source = Projection(
        identity=str(terms.source),
        governed_value="00042",
        knowledge=source_knowledge,
        capability_vocabulary=terms,
    )
    target = Projection(
        identity=str(terms.target),
        knowledge=target_knowledge,
        capability_vocabulary=terms,
    )

    relationship = projects_to(source=source, target=target)

    assert relationship.target_projection is not None, (
        "IT-2R3S2: The authorized projection must produce a target."
    )
    result = relationship.target_projection.knowledge
    assert result is not None, "IT-2R3S2: The target must retain its RDF knowledge."
    preserved_identity = (terms.target, terms.identityText, Literal("urn:example:publisher-a:00042"))
    assert preserved_identity in result, (
        "IT-2R3S2: The selected mapping convention must preserve the full "
        "qualified identity as target text; copying only 00042 loses meaning."
    )
    assert set(result.objects(terms.target, terms.identityText)) == {
        Literal("urn:example:publisher-a:00042")
    }, "IT-2R3S2: The mapped identity must equal the source identity."
    # The target's RDF knowledge carries the projection record. A requested
    # usesConvention link alone is not evidence that a convention was applied.
    assert (terms.target, terms.appliedConvention, terms.identityAsText) in result, (
        "IT-2R3S2: The projection record must identify the convention applied "
        "to preserve and interpret the required concept."
    )
