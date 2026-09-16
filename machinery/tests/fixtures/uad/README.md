# UAD XML Test Fixtures

This directory contains UAD appraisal XML samples used to test REFS projections of appraisal data into other knowledge representations, including RDF. UAD uses a subset of the MISMO reference model. These files are data instances, not MISMO schema definitions.

## Purpose

The initial use is **IT-2R2S2 — Preserve meaning across different projection types**, under **IT-2R2 — A projects-to relationship preserves required meaning**.

For a UAD XML-to-RDF example, the test must establish that a selected appraisal fact retains its meaning in the resulting RDF. Merely producing valid RDF, copying a string, or labeling a target as RDF does not establish that requirement.

The feature file defines the requirement. A fixture supplies a concrete example; the expected result states what the test must demonstrate.

## Available samples

| File | Sample indicated by filename |
| --- | --- |
| `2- to 4-unit_Appraisal_v1.4.xml` | 2- to 4-unit appraisal |
| `2- to 4-unit_Scenario_2_Appraisal_v1.2.xml` | 2- to 4-unit appraisal, scenario 2 |
| `Condo1_Appraisal_v1.4.xml` | Condominium appraisal, sample 1 |
| `Condo2_Appraisal_v1.4.xml` | Condominium appraisal, sample 2 |
| `Coop1_Appraisal_v1.4.xml` | Cooperative appraisal, sample 1 |

The samples were supplied as valid UAD XML. This README does not record an independent validation result. Filename suffixes such as `v1.4` are sample labels; they must not be assumed to identify the UAD release or MISMO schema version.

## Selecting an example

For each fixture used by a test, document:

- The file and applicable OTDD scenario identifier.
- The source element or attribute, identified by a namespace-aware XML path.
- The appraisal entity the value describes, such as the subject property or a comparable property.
- The source value and its relevant datatype, unit, or enumeration meaning.
- The expected RDF subject, predicate, and object, including datatype or language tag where applicable.
- The source-artifact and source-location links required to trace the projected fact back to the XML.

Select a real value from a sample and establish its mapping before implementing the projection. Preserve distinctions such as absent versus zero, and identifiers versus numbers. Do not assume that matching text always has the same meaning in different XML contexts.

## Expected results

Expected results are reviewed knowledge about the required projection. Write them independently of the implementation being tested. Do not generate the expected result with that implementation and then compare it to itself.

A small expected RDF graph may be stored in a corresponding `.ttl` file. Compare RDF meaning through graph assertions rather than serialization order or whitespace. The test must identify which facts are required; a small expected graph need not describe every fact in the complete appraisal.

No expected RDF files or approved XML-to-RDF mappings have been established in this directory yet.

## Source provenance

Before relying on a sample for a specific mapping, record its publisher, original source reference, sample release, applicable UAD/MISMO version, and available validation evidence. Those details are not established by this inventory.

Preserve the supplied XML samples. If a smaller excerpt is useful, save it as a separate fixture and document its parent file, extraction location, and changes. Do not describe an extracted fragment as a schema-valid complete appraisal unless that has been verified.

A fixture's local filename locates the test input; it does not replace its governed source identity or publisher provenance.

## Test conventions

Follow `OTDD-WORKING-CONVENTIONS.md` and the repository's feature files:

- Use pytest, with OTDD scenario identifiers in test names and useful failure messages.
- Locate fixtures relative to the test file, not an individual developer's absolute path.
- Keep test inputs stable; write generated outputs to pytest's `tmp_path`.
- Run the specific scenario during RED/GREEN work. Run regression at Rule completion unless a specific technical reason calls for an earlier run.

Although stored beside machinery tests, source examples and governed expectations contain knowledge. Executable requirements and knowledge about the process remain knowledge.
