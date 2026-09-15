# Generators

A **generator** is code that produces a knowledge artifact by applying
explicit rules to existing inputs.
Think of it as a builder: it takes recorded knowledge and instructions,
then constructs a defined result.
The term does not imply AI or permission to invent facts.

## Place in REFS Master KG

REFS uses one GitHub repository and one PyCharm project: `refs-master-kg`.
Generator code belongs under `machinery/generators/`; shared
implementation code belongs under `machinery/src/`, and implementation
tests under `machinery/tests/`.

Generated knowledge belongs in the appropriate knowledge area, such as
`gse-knowledge/` or `mismo-knowledge/`.
Declarative requirements in `features/` remain knowledge, even when
expressed as executable Gherkin. **Knowledge about knowledge is knowledge.**
Code implementing those requirements is machinery.

## Inputs and outputs

| Inputs                                                              | Outputs                                                       |
|---------------------------------------------------------------------|---------------------------------------------------------------|
| Harvested source assertions or other identified knowledge artifacts | Normalized knowledge records or explicitly derived assertions |
| Defined mapping, normalization, or inference rules                  | A record of the inputs and rules responsible for each result  |

Normalization puts knowledge into a consistent representation, such as
mapping source fields to REFS properties.
Derivation produces a conclusion or relationship by applying a rule.
A generator can also render existing knowledge into another format;
changing format alone does not create a new semantic assertion.

## Concrete REFS examples

These are illustrative responsibilities, not claims about existing
implementations:

- Take harvested MISMO element records and apply an explicit mapping to produce consistent REFS concept records in `mismo-knowledge/`, retaining the original source identifiers and definitions.
- Take harvested GSE requirements and an approved concept-mapping rule to produce links between those requirements and REFS concepts. Identify the links as REFS-derived rather than implying that the GSE published them.
- Produce a graph serialization from existing knowledge records while preserving assertion identities and provenance.

A [harvester](harvesters.md) captures a relationship explicitly stated
in a source.
A generator constructs a relationship through a REFS rule.
Similar wording alone is not sufficient evidence that two concepts are
equivalent.

## Role in OTDD

In REFS's OTDD workflow, a Feature, Rule, and Scenario define what the generated knowledge must satisfy. For example, a scenario in `features/IT-1-govern-source-identity-and-provenance.feature` could require distinguishing source-provided assertions from derived assertions.

A test under `machinery/tests/` supplies known inputs and a mapping rule, runs the generator, and checks both the resulting assertion and its derivation record. The Gherkin requirement remains knowledge; the generator and test implementation are machinery. A shared scenario identifier can connect the requirement, implementation, and evidence.

## Provenance expectations

Each generated result should be traceable through its inputs to the original sources. Retain:

- The identities and versions of the input records or artifacts.
- The mapping, normalization, or inference rule and its version.
- The generator version, relevant configuration, and generation run.
- Whether the result preserves a source assertion, normalizes its representation, or adds a derived assertion.

Preserve source-provided identifiers and distinguish them from REFS-assigned identifiers. Keep source assertions available separately from derived conclusions. Record assumptions and unresolved ambiguity; do not present generated conclusions as statements made by the source. Retain enough input and rule information to reproduce the result, and identify any non-deterministic steps.
