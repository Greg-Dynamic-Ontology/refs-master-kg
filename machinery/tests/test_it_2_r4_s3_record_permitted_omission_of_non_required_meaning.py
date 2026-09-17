"""IT-2R4S3: Record a permitted omission of non-required meaning.

RDF expectations permit omission of an optional note. The receiver requires the
identifier but cannot accept the governance record, which must remain in REFS
as a separate graph on the returned projects-to relationship.
"""

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import PROV, RDF

from machinery.src.projection import Projection, projects_to


def test_IT_2R4S3_record_permitted_omission_of_non_required_meaning():
    terms = Namespace("urn:refs:test:IT-2R4S3:")
    source_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R4S3:> .

        test:source
            test:containsMeaning test:identifier, test:optionalNote ;
            test:requiresMeaning test:identifier ;
            test:identifier "00042" ;
            test:optionalNote "Supporting note retained in REFS." .
        ''',
        format="turtle",
    )
    target_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R4S3:> .

        test:target
            test:usesFormat test:identifierFormat ;
            test:usesConvention test:identifierConvention ;
            test:usesExpectations test:receiverExpectations ;
            test:receiver test:device .

        test:device test:acceptsProjectionRecord false .

        test:identifierFormat
            test:capabilitiesComplete true ;
            test:supportsMeaning test:identifier .

        test:identifierConvention
            test:capabilitiesComplete true ;
            test:supportsMeaning test:identifier ;
            test:hasMapping test:identifierMapping .

        test:identifierMapping
            test:sourcePredicate test:identifier ;
            test:targetPredicate test:identifier .

        test:receiverExpectations
            test:requiresMeaning test:identifier ;
            test:nonRequiredMeaning test:optionalNote ;
            test:permitsOmission test:optionalNote .
        ''',
        format="turtle",
    )
    original_source = set(source_knowledge)
    source = Projection(
        identity=str(terms.source),
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
        "IT-2R4S3: The permitted projection must produce a target."
    )
    result = relationship.target_projection.knowledge
    assert result is not None, "IT-2R4S3: The target must retain its required knowledge."
    assert set(result.objects(terms.target, terms.identifier)) == {Literal("00042")}, (
        "IT-2R4S3: Required identifier meaning must be preserved."
    )
    assert not list(result.objects(terms.target, terms.optionalNote)), (
        "IT-2R4S3: The permitted optional note must be omitted from the target."
    )

    # The receiver cannot carry this record. Require a separate REFS graph,
    # rather than mistaking input permission declarations for an omission record.
    record = getattr(relationship, "projection_record", None)
    assert isinstance(record, Graph), (
        "IT-2R4S3: REFS must retain an omission record even when the receiver "
        "cannot accept it."
    )
    assert record is not result, (
        "IT-2R4S3: The REFS record must be separate from target knowledge."
    )
    omissions = {
        item for item in record.subjects(RDF.type, terms.PermittedOmission)
        if (item, terms.omittedMeaning, terms.optionalNote) in record
        and (item, terms.targetProjection, terms.target) in record
        and (item, RDF.subject, terms.source) in record
        and (item, RDF.predicate, terms.optionalNote) in record
        and (item, RDF.object, Literal("Supporting note retained in REFS.")) in record
    }
    assert omissions, (
        "IT-2R4S3: The record must identify the actual omitted source assertion "
        "and the target from which it was omitted."
    )
    assert any(
        (item, PROV.wasDerivedFrom, terms.source) in record
        and (item, terms.permittedBy, terms.receiverExpectations) in record
        for item in omissions
    ), (
        "IT-2R4S3: The omission must trace to its source and the expectations "
        "that permit it."
    )
    assert (terms.receiverExpectations, terms.permitsOmission, terms.optionalNote) in record, (
        "IT-2R4S3: The REFS record must retain the applicable permission."
    )
    assert not list(result.subjects(RDF.type, terms.PermittedOmission)), (
        "IT-2R4S3: Omission records must not be placed in the receiver's target knowledge."
    )
    assert set(source_knowledge) == original_source, (
        "IT-2R4S3: Omitting target meaning must not remove source evidence."
    )
