# OTDD plan to start the Processes
This is the right place to be very deliberate, because this is exactly
where we could accidentally recreate the IT-37 mistake at a larger scale.

The first feature files should not say “parse Excel,” “convert XSD,” or
“generate TTL.” 
Those are implementation moves. 
The first features need to define 
>**What it means for governed source evidence to become governed**
**knowledge in the REFS Master KG**.

We start with a small sequence like this:

```text
IT-1  Govern source identity and provenance
IT-2  Extract source assertions without losing source context
IT-3  Distinguish source assertions from derived knowledge
IT-4  Reconcile identities across source representations
IT-5  Admit governed domain knowledge into a component KG
IT-6  Integrate component knowledge into the REFS Master KG
IT-7  Project governed knowledge into downstream representations
```

That gives us a clean knowledge-construction spine.

The most important one is **IT-1**. I would make it something like:

```gherkin
Feature: Govern source knowledge entering the REFS Master KG

  As the REFS knowledge-construction process
  I want every harvested assertion to retain its governed source identity and provenance
  So that constructed knowledge remains traceable to authoritative evidence
```

Then the first Rules should establish things like:

```text
IT-1R1  A governed source artifact has an explicit identity
IT-1R2  A harvested assertion identifies the source artifact from which it was derived
IT-1R3  Source location within an artifact is preserved when available
IT-1R4  A source assertion is distinguishable from a derived assertion
IT-1R5  Reprocessing the same governed source does not create duplicate identities
```

Then **IT-2** can govern semantic extraction itself:

```gherkin
Feature: Extract semantic assertions from governed source representations

  As the REFS knowledge-construction process
  I want source representations to yield explicit semantic assertions
  So that knowledge implicit in documents, schemas, spreadsheets, and examples
  becomes computable without losing its governed meaning
```

Possible Rules:

```text
IT-2R1  A source representation may yield one or more semantic assertions
IT-2R2  Extracted assertions preserve source terminology
IT-2R3  Structural context needed to interpret an assertion is retained
IT-2R4  Missing source knowledge is not invented
IT-2R5  Equivalent source statements may later be reconciled without erasing provenance
```

Then **IT-3** becomes critical:

```gherkin
Feature: Distinguish source knowledge from constructed knowledge

  As the REFS knowledge-construction process
  I want direct source assertions and derived assertions to remain distinguishable
  So that users can determine what was published and what was inferred
```

That is where we prevent semantic laundering.

The architecture then becomes:

```text
governed source artifact
        ↓
source assertion graph
        ↓
identity/context reconciliation
        ↓
derived domain knowledge
        ↓
component KG
        ↓
REFS Master KG
        ↓
projection operators
```

And that, to me, is the first real KTDD/OTDD skeleton for `refs-master-kg`.

My recommendation: **begin with IT-1 only**. Write one feature file that governs source identity and provenance. Make the first Rule RED. Do not yet write extractors for Excel, XSD, PDF, or XML. Those should appear only when a feature forces them into existence.

That keeps us on the rails from the first line of this new project.