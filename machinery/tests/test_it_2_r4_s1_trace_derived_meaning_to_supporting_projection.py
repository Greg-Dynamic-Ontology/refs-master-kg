"""IT-2R4S1: Trace derived meaning to its supporting projection.

Synthetic RDF rule knowledge declares a classification implication. The mapper
must execute the selected rule and record assertion-level derivation provenance.
The test does not implement the inference or prepopulate its expected output.
"""

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, PROV

from machinery.src.projection import Projection, projects_to


def test_IT_2R4S1_trace_derived_meaning_to_supporting_projection():
    terms = Namespace("urn:refs:test:IT-2R4S1:")
    source_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R4S1:> .

        test:source a test:ResidentialMortgage ;
            test:containsMeaning test:classification ;
            test:requiresMeaning test:classification .
        ''',
        format="turtle",
    )
    target_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R4S1:> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

        test:target
            test:usesFormat test:rdfFormat ;
            test:usesConvention test:classificationConvention ;
            test:usesPreferences test:selectedPreferences .

        test:rdfFormat
            test:capabilitiesComplete true ;
            test:supportsMeaning test:classification .

        test:classificationConvention
            test:capabilitiesComplete true ;
            test:supportsMeaning test:classification ;
            test:hasDerivationRule test:mortgageIsLoan .

        test:selectedPreferences
            test:enablesRule test:mortgageIsLoan .

        test:mortgageIsLoan a test:DerivationRule ;
            test:premisePredicate rdf:type ;
            test:premiseObject test:ResidentialMortgage ;
            test:conclusionPredicate rdf:type ;
            test:conclusionObject test:Loan .
        ''',
        format="turtle",
    )
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
        "IT-2R4S1: The projection must produce a target."
    )
    result = relationship.target_projection.knowledge
    assert result is not None, "IT-2R4S1: The target must retain its RDF knowledge."
    assert (terms.target, RDF.type, terms.Loan) in result, (
        "IT-2R4S1: The selected RDF derivation rule must add the supported "
        "Loan classification to the target."
    )

    # Identify the exact derived assertion, without prescribing its generated ID.
    records = {
        record
        for record in result.subjects(RDF.type, terms.DerivedAssertion)
        if (record, RDF.subject, terms.target) in result
        and (record, RDF.predicate, RDF.type) in result
        and (record, RDF.object, terms.Loan) in result
    }
    assert records, (
        "IT-2R4S1: The added classification must be explicitly identifiable "
        "as a derived assertion."
    )
    traced_records = {
        record for record in records
        if (record, PROV.wasDerivedFrom, terms.source) in result
    }
    assert traced_records, (
        "IT-2R4S1: The derived assertion must trace to its supporting source projection."
    )
    activities = {
        activity
        for record in traced_records
        for activity in result.objects(record, PROV.wasGeneratedBy)
        if (activity, RDF.type, PROV.Activity) in result
    }
    assert any(
        (activity, PROV.used, terms.source) in result
        and (activity, PROV.used, terms.mortgageIsLoan) in result
        and (activity, PROV.used, terms.selectedPreferences) in result
        for activity in activities
    ), (
        "IT-2R4S1: The derivation record must identify the source, derivation "
        "rule, and mapping preferences actually applied to this assertion."
    )
