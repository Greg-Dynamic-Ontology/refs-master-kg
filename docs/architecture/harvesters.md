# Harvesters

A **harvester** is code that collects knowledge already present in a
source and records it in a form REFS can use. 
Think of it as a careful reader that brings back both the information
and its source reference.

## Place in REFS Master KG

REFS uses one GitHub repository and one PyCharm project:
`refs-master-kg`.
Harvester code belongs under `machinery/harvesters/`; shared
implementation code belongs under `machinery/src/`, and implementation
tests under `machinery/tests/`.

The knowledge it collects belongs in the appropriate knowledge area,
such as `gse-knowledge/` or `mismo-knowledge/`.
Requirements in `features/` are also knowledge: they describe what must
be true of REFS knowledge and its governance.
Executable Gherkin does not become mere machinery.
**Knowledge about knowledge is knowledge.**

## Inputs and outputs

| Inputs                                                                                           | Outputs                                                                                      |
|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| An identified source, such as a GSE guide or MISMO schema, with its version or retrieval context | Records of the definitions, identifiers, relationships, or requirements found in that source |
| Rules identifying the content to collect                                                         | Source references and extraction details supporting each collected assertion                 |

A harvester may parse a document or change its storage format. Its defining job is to preserve what the source says. It must not silently turn an interpretation into a source-provided fact.

## Concrete REFS examples

These are illustrative responsibilities, not claims about existing
implementations:

- Read a GSE guide section and capture a defined term or stated
requirement, retaining the guide edition and section reference in
`gse-knowledge/`.
- Read a MISMO schema and capture an element's source-provided name, 
identifier when available, definition, and declared relationships in
`mismo-knowledge/`.

Deciding that two differently named terms mean the same thing is a
separate derivation. That belongs to a [generator](generators.md), 
with the mapping rule and its evidence recorded.

## Role in OTDD

In REFS's OTDD workflow, a Feature, Rule, and Scenario state the
required knowledge behavior; machinery implements and checks it.
For example, a scenario in
`features/IT-1-govern-source-identity-and-provenance.feature`
could require retaining a source-provided identifier when one exists. 
The harvester captures that identifier, and a test under
`machinery/tests/` checks the resulting knowledge record against the
requirement.

The scenario is knowledge about governance.
The harvester and test runner are machinery.
Their shared scenario identifier can connect the requirement,
implementation, and evidence.

## Provenance expectations

Each harvested assertion should be traceable to the source that supports
it. Retain:

- Source identity, including its source-provided identifier when
available.
- Source version or edition, retrieval time, and a precise location
such as a section, page, or schema path.
- The source content or a stable reference to a retained copy sufficient
to check the extraction.
- The harvester version and collection run, including any extraction
limitations.

Distinguish identifiers supplied by the source from identifiers assigned
by REFS.
Mark collected assertions as source-provided, and keep any added
interpretation distinguishable.
If extraction is uncertain, record that uncertainty rather than
inventing a fact.
