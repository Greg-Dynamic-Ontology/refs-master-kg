"""IT-2R3S3: Reject a serialization that cannot preserve required named graphs.

The same assertion occurs in two named graphs. Flattening them would erase the
distinction between their graph memberships. Synthetic RDF declarations identify
both required graphs and the complete capabilities of the target and convention.
"""

import pytest
from rdflib import Dataset, Graph, Literal, Namespace

from machinery.src.projection import Projection, projects_to


def test_IT_2R3S3_reject_serialization_that_cannot_preserve_required_named_graphs():
    terms = Namespace("urn:refs:test:IT-2R3S3:")
    source_knowledge = Dataset()
    source_knowledge.default_graph.parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R3S3:> .

        test:source
            test:containsMeaning test:namedGraphDistinctions ;
            test:requiresMeaning test:namedGraphDistinctions ;
            test:requiresNamedGraph test:publisherA, test:publisherB .

        ''',
        format="turtle",
    )
    # Construct graph membership directly, avoiding deprecated TriG parser calls.
    assertion = (terms.loan, terms.eligible, Literal(True))
    for graph_id in (terms.publisherA, terms.publisherB):
        source_knowledge.graph(graph_id).add(assertion)
    target_knowledge = Graph().parse(
        data='''
        @prefix test: <urn:refs:test:IT-2R3S3:> .

        test:target
            test:usesFormat test:singleGraphSerialization ;
            test:usesConvention test:noGraphEncoding .

        test:singleGraphSerialization
            test:capabilitiesComplete true ;
            test:supportsMeaning test:rdfTriples .

        test:noGraphEncoding
            test:capabilitiesComplete true ;
            test:supportsMeaning test:rdfTriples .
        ''',
        format="turtle",
    )
    # Verify that the fixture contains real graph memberships, not just labels.
    for graph_id in (terms.publisherA, terms.publisherB):
        assert assertion in source_knowledge.graph(graph_id), (
            f"IT-2R3S3: Fixture must contain the assertion in {graph_id}."
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

    try:
        projects_to(source=source, target=target)
    except ValueError as rejection:
        reason = str(rejection)
        assert str(terms.namedGraphDistinctions) in reason, (
            "IT-2R3S3: The rejection must identify unsupported named graph distinctions."
        )
        for graph_id in (terms.publisherA, terms.publisherB):
            assert str(graph_id) in reason, (
                "IT-2R3S3: The rejection must identify each required named graph "
                f"whose distinction cannot be preserved; missing {graph_id}."
            )
    else:
        pytest.fail(
            "IT-2R3S3: Reject the serialization when the selected convention "
            "cannot preserve the required named graph distinctions."
        )
