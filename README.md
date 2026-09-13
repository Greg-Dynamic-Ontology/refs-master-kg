# REFS Master KG

## Real Estate Finance System Master Knowledge Graph

`refs-master-kg` is a Knowledge Test-Driven Development (KTDD) and Ontology Test-Driven
Development (OTDD) project for constructing a governed knowledge graph for the Real Estate
Finance industry.
It encompasses all the stages creating, packaging, selling, servicing and payment processing
aspects of the industry.

The project begins with the Uniform Appraisal Dataset (UAD), but UAD is not the boundary of
the project. 
UAD is the first substantial proving ground for constructing, governing, testing, integrating,
and projecting knowledge from the broader real estate finance ecosystem.

The long-term goal is a **REFS Master Knowledge Graph** in which important industry
relationships become computable rather than remaining implicit across schemas, spreadsheets,
specifications, implementation guides, business rules, examples, scenarios, software, and
human expertise.

## Motivation

The project grows from a simple observation:

> XML is a tree, but the world is not.

An XSD can represent substantial structural knowledge, but it cannot hold all of the knowledge
required to understand and use a real business domain.

The same limitation applies to every individual representation. A spreadsheet can express rules
absent from an XSD. 
A reference guide can supply meaning absent from both. Sample instances demonstrate contexts
and relationships. 
Scenario matrices relate data points to business situations.
Publication history provides provenance. 
Tests and executable rules express still other projections of the domain.

The governing idea is:

> **Knowledge is primary. Documents, schemas, rules, code, and tests are projections of
> knowledge.**

```text
Knowledge
    +-- projection --> document
    +-- projection --> schema
    +-- projection --> rule
    +-- projection --> code
    +-- projection --> test
```

A projection is useful, but it must not be confused with the knowledge being projected.

## Why UAD First?

UAD is an unusually rich KTDD/OTDD test bed.

Fannie Mae and Freddie Mac publish governed artifacts describing overlapping facets of UAD,
including XML schemas, delivery specifications, implementation guides, reference guides,
compliance-rule spreadsheets, cross-reference material, report layouts, scenario matrices,
sample XML instances, and versioned publications.

UAD is based on a subset of the MISMO 3.6 schema while adding GSE-specific requirements,
contexts, constraints, examples, and implementation knowledge.

No single artifact is UAD knowledge. 
Together, these governed sources provide evidence from which a richer UAD knowledge
representation can be constructed.

## Beyond UAD

UAD is one member of a larger family of GSE uniformity initiatives. 
The project structure anticipates additional domains such as UCD, ULAD, and ULDD.

The project also recognizes MISMO as a broader industry knowledge source. 
The expected direction is progressively connected governed knowledge:

```text
MISMO knowledge -----------+
                           |
GSE knowledge -------------+--> domain knowledge --> REFS Master KG
                           |
other governed knowledge --+
```

## Project Structure

The initial project structure is intentionally small:

```text
refs-master-kg/
|-- features/
|-- gse-knowledge/
|   |-- UAD/
|   |   |-- fannie-mae/
|   |   `-- freddie-mac/
|   |-- UCD/
|   |   |-- fannie-mae/
|   |   `-- freddie-mac/
|   |-- ULAD/
|   |   |-- fannie-mae/
|   |   `-- freddie-mac/
|   `-- ULDD/
|       |-- fannie-mae/
|       `-- freddie-mac/
|-- knowledge-tools/
|-- master-knowledge/
|-- mismo-knowledge/
|-- tests/
`-- uad-knowledge/
```

Additional structure will be introduced only when required by governed behavior and tests.

### `features/`

Contains KTDD/OTDD behavioral specifications. 
Knowledge construction is governed through Features, Rules, and Scenarios rather than being
allowed to emerge accidentally from implementation code.

The project follows the OTDD practice:

> **Commit at Rule breaks.**

### `gse-knowledge/`

Contains governed source evidence obtained from Fannie Mae and Freddie Mac.

Publisher identity is preserved even when the GSEs publish equivalent or identical artifacts.
Provenance is knowledge and must not be erased merely because two files happen to contain the
same information.

Downloaded archive files need not be committed when their verified extracted contents are the
governed project inputs and the original publication packages are preserved separately.

### `mismo-knowledge/`

Contains governed MISMO source knowledge and material derived specifically from MISMO sources.

MISMO represents a broader real estate finance domain than UAD. UAD uses a governed subset of
MISMO schema knowledge rather than constituting an independent schema universe.

### `uad-knowledge/`

Contains knowledge constructed specifically for UAD from relevant MISMO and GSE source evidence.

This is distinct from `gse-knowledge/`: the GSE directories preserve source evidence;
`uad-knowledge/` contains governed knowledge constructed from that evidence.

### `master-knowledge/`

Contains the integrated REFS Master Knowledge Graph or its governed component graphs.

This is the knowledge space in which relationships can cross individual source documents,
publishers, GSE programs, and domain boundaries.

The Master KG need not be one undifferentiated Turtle file. It may consist of governed
component or named graphs whose identities and provenance are preserved while participating
in one logical knowledge space.

### `knowledge-tools/`

Contains software that operates on governed knowledge.

Tools may harvest knowledge from governed sources, construct RDF, reconcile identities, relate
knowledge across source representations, insert or remove knowledge, determine implication,
project knowledge into other representations, and serialize graphs.

Tools operate on knowledge. They are not themselves the knowledge being governed.

### `tests/`

Contains executable tests proving that governed knowledge is captured, transformed, preserved,
related, and projected correctly.
We use Python and pytest to control the execution of the tests.
However the goal of the project is NOT to produce Python executable code, but to produce the knowledge
artifacts.

Knowledge will be represented using RDF and related W3C standards with a sprinkling of the domain
identifiers of Dynamic Knowledge Growth Associates, LLC.

## KTDD and OTDD

This project is developed using Knowledge Test-Driven Development.

> **KTDD is test-driven development in which knowledge is a first-class development artifact,
> and tests establish that knowledge is correctly captured, transformed, preserved, applied, and
> produced.**

Ontology Test-Driven Development is the specialization of KTDD concerned specifically with
constructing and evolving ontologies and ontological commitments.

The project follows RED/GREEN discipline:

```text
governed requirement
        |
        v
behavioral specification
        |
        v
RED test
        |
        v
smallest implementation
        |
        v
GREEN test
        |
        v
regression
        |
        v
Rule-break commit
```

The project structure itself should evolve through this process. Directories and implementation
machinery should not be created merely because they seem likely to be useful later.

## Governed Sources and Constructed Knowledge

A fundamental distinction is maintained between **source evidence** and **constructed knowledge**.

Governed sources may include material published by MISMO, Fannie Mae, Freddie Mac, and other
authoritative organizations. Constructed knowledge may combine facts and relationships discovered
across those sources.

The derivation must remain traceable:

```text
governed source evidence
        |
        v
knowledge construction
        |
        v
governed knowledge
        |
        v
projection operators
        |
        +--> SHACL
        +--> tests
        +--> documentation
        +--> APIs
        +--> software behavior
        +--> AI context
```

The source publication is not replaced by the knowledge graph.
It remains evidence supporting the knowledge represented in the graph.

## Projection Rather Than Duplication

A central architectural principle is:

> **Knowledge -> projection operator -> representation**

A SHACL shape, test case, document, API response, or program should therefore be understood as
a projection produced for a particular purpose.

This permits multiple products to consume the same governed knowledge without independently
reconstructing the domain.

UAD knowledge may eventually support a UAD validation service, UAD service tester, constraint
production, controlled mutation of GSE sample XML, specification exploration, publication change analysis, a knowledge API, third-party validator conformance testing, and bounded domain context for AI systems.

## Computable Industry Knowledge

The value of an industry knowledge graph is not the number of triples it contains.
Its value is that relationships that previously existed only implicitly in documents and computer
code can become computable.

One important example is change-impact analysis:

```text
MISMO concept
    |
    v
UAD schema usage
    |
    v
GSE data point
    |
    v
compliance rule
    |
    v
report context
    |
    v
sample scenario
    |
    v
XML example
    |
    v
validation test
```

Instead of asking experts to manually discover the consequences of a standards change across many
representations, affected knowledge can be traversed computationally.

Other potential computations include coverage, equivalence, dependency, consistency, provenance,
and the blast radius of specification changes.

## UAD Service Testing

GSE sample scenarios are more than example files.

Scenario matrices can provide relationships among sample files, appraisal scenarios, and data
points.
Those relationships allow a future UAD Service Tester to select meaningful test combinations
rather than generating a Cartesian product of every sample file and every data point.

```text
sample XML
    |
    v
scenario
    |
    v
related data point
    |
    v
governing constraint
    |
    v
controlled mutation
    |
    v
expected finding
```

The knowledge graph should tell the tester which experiments are meaningful.

## Product Direction

The REFS Master KG is intended to become a reusable knowledge asset rather than an implementation
detail of a single application.

The UAD validator can become its first proving consumer.

Over time, the same governed knowledge may support other validation providers and other real
estate finance systems. 
A third-party validator need not adopt our validation engine to consume computable UAD 
knowledge, change intelligence, constraint definitions, or conformance tests.

The broader proposition is:

> **Provide computable real estate finance knowledge and evidence that implementations conform
> to it.**

The organizations publishing the underlying standards and specifications remain the authoritative
sources. 
The value added by this project is the governed integration, relationships, testing, provenance,
and computable projections constructed from those sources.

## Guiding Principles

1. **Knowledge is the asset.**
2. **A representation is a projection of knowledge, not the knowledge itself.**
3. **A tree is a projection of a graph, not a substitute for one.**
4. **Governed source identities should be preserved whenever they exist.**
5. **Generated identities are fallbacks, not defaults.**
6. **Provenance is knowledge.**
7. **Source evidence and derived knowledge must remain distinguishable.**
8. **Knowledge construction must be test driven.**
9. **Agents and tools operate on governed knowledge through explicit contracts.**
10. **When knowledge is insufficient to support a conclusion, return an exception rather than
inventing one.**
11. **The statistical component may choose only among graph-permitted alternatives.**
12. **Software is one representation of knowledge.**
13. **Derivation, not divination.**

## Current Scope

The immediate objective is deliberately narrower than the long-term REFS vision:

> **Construct and govern the UAD knowledge needed to prove the REFS Master KG architecture.**

The next work should begin with a KTDD/OTDD Feature defining what it means for governed source
knowledge to become part of the Master KG.

The implementation follows from that knowledge behavior, not the other way around.
