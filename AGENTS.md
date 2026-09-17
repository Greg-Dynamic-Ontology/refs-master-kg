# Instructions for work in refs-master-kg

## Required working conventions

Before beginning or resuming work, read:

C:/Users/grego/projects/OTDD-WORKING-CONVENTIONS.md

Follow those conventions throughout the task. If the file cannot be read,
report that before editing repository files.

## No-surprises workflow

Before editing repository files:
- Identify the files to be changed.
- Identify the tests to be run.
- Explain any proposed departure from the established workflow.

Afterward:
- Report the files actually changed.
- Report the tests run and their results.
- Distinguish repository changes from downloadable drafts.

Announce workflow changes before applying them.

## OTDD

The repository and accepted feature files are authoritative.

Follow Feature → Rule → Scenario → RED → GREEN.

When asked to make a scenario RED, stop after establishing and reporting
RED. Do not implement GREEN until instructed.

When the user confirms RED, treat that as confirmation of their execution,
not as a request to reconfirm it.

Use Windows CMD.exe and pytest. Provide the exact command for running the
specific test. Follow the shared conventions for regression and commits.

## Knowledge and machinery

Features, mapping rules, mapping preferences, and governance policies are
knowledge artifacts. Executable requirements remain knowledge.

Represent mapping and process knowledge in RDF rather than embedding
fixture-specific decisions in operational code.

Operational code and tests belong under machinery/.