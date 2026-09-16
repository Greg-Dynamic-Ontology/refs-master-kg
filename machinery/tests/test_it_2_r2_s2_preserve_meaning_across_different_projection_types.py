"""IT-2R2S2 — Preserve meaning across different projection types.

IT-2R2 — A projects-to relationship preserves required meaning.

Compare the supplied XML and RDF projections across all eight value kinds.
This checks the supplied representations, not an XML-to-RDF conversion engine.
The same test is RED without its fixtures and GREEN when their meanings agree.
"""

from datetime import date
from decimal import Decimal
from pathlib import Path
import xml.etree.ElementTree as ET

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, SKOS, XSD


FX = Namespace("urn:refs:fixture-vocabulary:")
FIXTURES = Path(__file__).parent / "fixtures" / "uad"
SCENARIO = "IT-2R2S2"


def one(graph, subject, predicate):
    values = list(graph.objects(subject, predicate))
    assert len(values) == 1, (
        f"{SCENARIO}: Expected one {predicate} for {subject}; found {values}."
    )
    return values[0]


def typed_value(graph, subject, predicate, datatype):
    value = one(graph, subject, predicate)
    assert isinstance(value, Literal) and value.datatype == datatype, (
        f"{SCENARIO}: {predicate} must have RDF datatype {datatype}; found {value!r}."
    )
    return value.toPython()


def test_IT_2R2S2_preserve_meaning_across_projection_types():
    xml_file = FIXTURES / "data-test-it2r2s2.xml"
    rdf_file = FIXTURES / "data-test-it2r2s2.ttl"
    missing = [path.name for path in (xml_file, rdf_file) if not path.is_file()]
    assert not missing, f"{SCENARIO}: Missing projection fixtures: {', '.join(missing)}"

    root = ET.parse(xml_file).getroot()
    graph = Graph().parse(rdf_file, format="turtle")
    properties = root.findall("PROPERTY")
    assert len(properties) == 1, f"{SCENARIO}: This fixture must contain one XML property."
    xml_property = properties[0]
    rdf_properties = list(graph.subjects(RDF.type, FX.Property))
    assert len(rdf_properties) == 1, f"{SCENARIO}: RDF must represent one property."
    rdf_property = rdf_properties[0]
    address = one(graph, rdf_property, FX.address)
    detail = one(graph, rdf_property, FX.comparableDetail)
    xml_detail = xml_property.find("COMPARABLE/COMPARABLE_DETAIL")
    assert xml_detail is not None, f"{SCENARIO}: XML comparable detail is missing."

    # Identifier and text remain strings attached to the correct address.
    for predicate, xml_path in (
        (FX.addressUnitIdentifier, "ADDRESS/AddressUnitIdentifier"),
        (FX.cityName, "ADDRESS/CityName"),
    ):
        assert typed_value(graph, address, predicate, XSD.string) == xml_property.findtext(xml_path), (
            f"{SCENARIO}: Identifier/text meaning changed at {xml_path}."
        )

    # Measurement retains both decimal value and its source-specified unit.
    xml_measure = xml_detail.find("ProximityToSubjectDistanceLinearMeasure")
    assert xml_measure is not None, f"{SCENARIO}: XML measurement is missing."
    measurement = one(graph, detail, FX.proximityToSubjectDistance)
    assert typed_value(graph, measurement, RDF.value, XSD.decimal) == Decimal(xml_measure.text), (
        f"{SCENARIO}: Decimal measurement changed."
    )
    unit = one(graph, measurement, FX.linearUnitOfMeasureType)
    assert str(one(graph, unit, SKOS.notation)) == xml_measure.get("LinearUnitOfMeasureType"), (
        f"{SCENARIO}: Measurement unit changed."
    )

    xml_boolean = xml_detail.findtext("NoFinancingTransactionIndicator")
    assert xml_boolean in ("true", "false"), f"{SCENARIO}: Explicit XML Boolean required."
    assert typed_value(graph, detail, FX.noFinancingTransactionIndicator, XSD.boolean) == (
        xml_boolean == "true"
    ), f"{SCENARIO}: Boolean meaning changed."

    # Enumeration codes retain their values and code-system context.
    for subject, predicate, scheme, expected in (
        (address, FX.stateCode, FX.StateCodes, xml_property.findtext("ADDRESS/StateCode")),
        (rdf_property, FX.valuationUseType, FX.ValuationUseTypes, xml_property.get("ValuationUseType")),
    ):
        concept = one(graph, subject, predicate)
        assert str(one(graph, concept, SKOS.notation)) == expected, (
            f"{SCENARIO}: Enumeration value changed."
        )
        assert (concept, SKOS.inScheme, scheme) in graph, (
            f"{SCENARIO}: Enumeration scheme changed."
        )

    # Dates and amounts must remain paired with their respective repeated records.
    xml_histories = xml_property.findall("SALES_HISTORIES/SALES_HISTORY")
    rdf_histories = list(graph.objects(rdf_property, FX.salesHistory))
    assert len(xml_histories) >= 2, f"{SCENARIO}: Repeated XML records are required."
    assert len(rdf_histories) == len(xml_histories), f"{SCENARIO}: Sales-history count changed."
    expected_records = {
        (i, date.fromisoformat(h.findtext("OwnershipTransferDate")),
         Decimal(h.findtext("OwnershipTransferTransactionAmount")))
        for i, h in enumerate(xml_histories, 1)
    }
    actual_records = {
        (typed_value(graph, h, FX.sourcePosition, XSD.integer),
         typed_value(graph, h, FX.ownershipTransferDate, XSD.date),
         typed_value(graph, h, FX.ownershipTransferTransactionAmount, XSD.decimal))
        for h in rdf_histories
    }
    assert actual_records == expected_records, (
        f"{SCENARIO}: Dates, monetary amounts, or repeated-record associations changed."
    )
