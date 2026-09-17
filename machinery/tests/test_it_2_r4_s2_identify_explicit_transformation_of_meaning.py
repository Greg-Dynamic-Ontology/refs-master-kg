"""IT-2R4S2: Identify an explicit transformation of meaning.

Synthetic RDF knowledge explicitly translates a source code to a target status.
The test requires the actual output and assertion-level provenance; merely
copying the transformation declaration into the target is insufficient.
"""

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import PROV, RDF

from machinery.src.projection import Projection, projects_to


def test_IT_2R4S2_identify_explicit_transformation_of_meaning():
    terms = Namespace("urn:refs:test:IT-2R4S2:")
    source_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R4S2:> .

        test:source
            test:containsMeaning test:decisionStatus ;
            test:requiresMeaning test:decisionStatus ;
            test:decisionCode "A1" .
        ''',
        format="turtle",
    )
    target_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R4S2:> .

        test:target
            test:usesFormat test:rdfFormat ;
            test:usesConvention test:statusConvention ;
            test:usesPreferences test:selectedPreferences .

        test:rdfFormat
            test:capabilitiesComplete true ;
            test:supportsMeaning test:decisionStatus .

        test:statusConvention
            test:capabilitiesComplete true ;
            test:supportsMeaning test:decisionStatus ;
            test:hasTransformationRule test:translateStatus .

        test:selectedPreferences test:enablesRule test:translateStatus .

        test:translateStatus a test:TransformationRule ;
            test:premisePredicate test:decisionCode ;
            test:premiseObject "A1" ;
            test:conclusionPredicate test:decisionStatus ;
            test:conclusionObject "Accepted" .
        ''',
        format="turtle",
    )
    source_before = set(source_knowledge)
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
        "IT-2R4S2: The projection must produce a target."
    )
    result = relationship.target_projection.knowledge
    assert result is not None, "IT-2R4S2: The target must retain its RDF knowledge."
    assert set(result.objects(terms.target, terms.decisionStatus)) == {
        Literal("Accepted")
    }, (
        "IT-2R4S2: The selected RDF transformation rule must translate "
        "source code A1 to target status Accepted."
    )
    records = {
        record
        for record in result.subjects(RDF.type, terms.TransformedAssertion)
        if (record, RDF.subject, terms.target) in result
        and (record, RDF.predicate, terms.decisionStatus) in result
        and (record, RDF.object, Literal("Accepted")) in result
    }
    assert records, (
        "IT-2R4S2: The target status assertion must be explicitly identified "
        "as transformed."
    )
    traced_records = {
        record for record in records
        if (record, PROV.wasDerivedFrom, terms.source) in result
    }
    assert traced_records, (
        "IT-2R4S2: The transformed assertion must trace to its source projection."
    )
    activities = {
        activity
        for record in traced_records
        for activity in result.objects(record, PROV.wasGeneratedBy)
        if (activity, RDF.type, PROV.Activity) in result
    }
    assert any(
        (activity, PROV.used, terms.source) in result
        and (activity, PROV.used, terms.translateStatus) in result
        and (activity, PROV.used, terms.selectedPreferences) in result
        for activity in activities
    ), (
        "IT-2R4S2: The transformation record must identify the source, rule, "
        "and preferences actually applied to this assertion."
    )
    assert set(source_knowledge) == source_before, (
        "IT-2R4S2: The original source evidence must remain unchanged."
    )
