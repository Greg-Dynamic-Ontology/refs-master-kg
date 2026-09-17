# REFS Policy: JSON and JSON-LD Projections

## Purpose

REFS projections must preserve the meaning required for their intended use.
A projection’s suitability depends on its format, its governing standards, and
the mapping rules and preferences used to interpret it.

This policy distinguishes ordinary JSON integration from JSON-LD serialization of
governed knowledge.

## Ordinary JSON

### Permitted only for necessary outbound integration

Ordinary JSON may be used as a target when a specified receiving device or external
system requires JSON and offers no supported alternative that meets the integration
requirements.

Developer convenience or preference alone does not qualify.

The projection record must identify:

- The receiving device or system.
- Its applicable interface specification and version.
- Why no supported alternative meets the requirement.
- The mapping rules and conventions used.

The justification must be reviewed when the receiving interface changes.

### Preservation of required meaning

Required meaning must be established for the intended use before the projection is
approved.
A device-specific output need not contain the entire REFS knowledge graph, but it must
preserve everything required for that use.

A projection that would lose required meaning must be rejected. Any permitted omission
of non-required meaning must be identified and recorded in REFS, together with the
applicable governed expectations.

The receiving system need not accept this accompanying governance record.

### Unsupported as a knowledge source

Projection from ordinary JSON into REFS governed knowledge is outside the supported scope.

Reading operational acknowledgments or error responses from an authorized integration
does not, by itself, constitute admitting JSON as a source of governed knowledge.

### No guarantee of reversibility

An ordinary JSON target carries no guarantee that the original source knowledge can be
reconstructed.
An outbound integration does not establish a supported reverse projection.

## JSON-LD

### Allowed as a knowledge target

JSON-LD is an allowed target serialization for REFS knowledge.
It is governed separately from ordinary JSON because it provides a standardized
interpretation of linked data and supports RDF serialization.

A JSON-LD projection must preserve the governed RDF graph or dataset required for its use.

### Context and interpretation

The contexts, vocabulary identifiers, and processing conventions needed to interpret a
JSON-LD projection must be identified and retained or resolvable through governed
references.

The projection must not depend on undocumented assumptions or uncontrolled changes to
external context definitions.

### Conversion and reversibility

Conversion between JSON-LD and another standardized knowledge serialization is supported
when both can represent the same governed knowledge without loss.

Reversibility concerns the RDF graph or dataset.
It does not require reproducing the original formatting, property order, compact field
names, or document layout.

The selected serialization must support the constructs being preserved.
For example, a dataset containing named graphs requires a dataset-capable serialization.

Permission to produce JSON-LD does not automatically authorize all JSON-LD inputs.
Admission as a source remains subject to applicable source-governance requirements.

## Transport Envelopes

A JSON envelope carrying an intact RDF document is treated as transport when the
enclosed document retains its governed interpretation.

The envelope must not alter, discard, or ambiguously reinterpret the enclosed knowledge.

## Mapping Governance

Mapping rules and preferences are shared, governed knowledge.
They must identify how source meaning is represented within the capabilities of the
target format and its applicable conventions.

Preferences cannot override this policy.
Where the target cannot preserve required meaning, the projection must be rejected
rather than silently weakened.

Projection records must retain the source references, applicable mapping knowledge, and
any declared transformations or permitted omissions needed to explain the result.

## Implementation and Verification

This policy, its RDF representation, and its Gherkin requirements are knowledge artifacts.

Operational code and tests under `machinery/` enforce and verify the policy, including:

- Restricting ordinary JSON targets to justified integrations.
- Rejecting unsupported ordinary JSON source projections.
- Preserving required meaning.
- Recording permitted omissions.
- Preserving governed RDF meaning in JSON-LD.
- Checking reversibility against the capabilities of the selected serializations.

## Standard Reference

[W3C JSON-LD 1.1](https://www.w3.org/TR/json-ld11/), including its specification of the
relationship between JSON-LD and RDF.