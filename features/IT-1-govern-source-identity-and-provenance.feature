@IT-1
Feature: Govern source identity and provenance

  The REFS Master Knowledge Graph is constructed from governed source
  artifacts published by authoritative organizations.

  Knowledge constructed from those artifacts must remain traceable to
  the evidence from which it was derived.

  Source identity and provenance must therefore be established before
  semantic extraction or integration into the REFS Master Knowledge Graph.

  @IT-1R1
  Rule: Governed source identity is preserved when provided by the governing source

    @IT-1R1S1
    Scenario: Preserve a source-provided identity
      Given a governed source artifact with an identity provided by its governing source
      When the artifact is admitted as REFS source evidence
      Then the source-provided identity is preserved

    @IT-1R1S2
    Scenario: Register one governed source artifact
      Given a governed source artifact
      When the artifact is admitted as REFS source evidence
      Then the artifact has one governed identity
      And the identity is associated with the governing source

    @IT-1R1S3
    Scenario: Reuse the governed identity for the same source artifact
      Given a governed source artifact already admitted as REFS source evidence
      When the same source artifact is encountered again
      Then the existing governed identity is reused
      And no second governed identity is created

    @IT-1R1S4
    Scenario: Distinguish different governed source artifacts
      Given two different governed source artifacts
      When both artifacts are admitted as REFS source evidence
      Then each artifact has its own governed identity
      And the two governed identities are different

  @IT-1R2
  Rule: A governed source artifact retains its provenance

    @IT-1R2S1
    Scenario: Preserve the publisher boundary
      Given Fannie Mae publishes a constraint
        And Freddie Mac publishes an equivalent constraint
        When REFS represents their shared requirement as a GSE constraint
        Then the Fannie Mae source constraint remains identifiable
        And the Freddie Mac source constraint remains identifiable
        And the GSE constraint retains a link to each source constraint

    @IT-1R2S2
    Scenario: Preserve the publisher boundary
      Given governed source artifacts published by different authoritative organizations
      When the artifacts are admitted as REFS source evidence
      Then each artifact retains its publisher provenance
      And equivalent content does not erase the publisher boundary

    @IT-1R2S3
    Scenario: Preserve publication identity independently of local storage
      Given a governed source artifact stored in the REFS project
      When the artifact is admitted as REFS source evidence
      Then its governed identity does not depend on its local filesystem path

  @IT-1R3
  Rule: Knowledge derived from a source artifact remains traceable to that artifact

    @IT-1R3S1
    Scenario: Trace a source assertion to its source artifact
      Given a governed source artifact
      And an assertion extracted directly from that artifact
      When the assertion is represented as REFS knowledge
      Then the assertion identifies the source artifact from which it was derived

    @IT-1R3S2
    Scenario: Preserve source location when the source provides one
      Given an assertion extracted from an identifiable location within a governed source artifact
      When the assertion is represented as REFS knowledge
      Then the assertion retains the identifiable source location

    @IT-1R3S3
    Scenario: Trace independently published assertions independently
      Given equivalent assertions extracted from artifacts published by different authoritative organizations
      When the assertions are represented as REFS knowledge
      Then each assertion remains traceable to its own source artifact

  @IT-1R4
  Rule: Source assertions remain distinguishable from derived assertions

    @IT-1R4S1
    Scenario:  Identify an assertion stated by a governed source
      Given an assertion extracted directly from a governed source artifact
      When the assertion is represented as REFS knowledge
      Then it is identifiable as a source assertion

    @IT-1R4S2
    Scenario:  Identify an assertion derived from governed knowledge
      Given an assertion derived from one or more governed assertions
      When the derived assertion is represented as REFS knowledge
      Then it is identifiable as a derived assertion
      And its derivation is traceable to the governed assertions used to derive it

    @IT-1R4S3
    Scenario: Do not represent a derived assertion as a source assertion
      Given an assertion not explicitly stated by a governed source artifact
      When the assertion is derived during knowledge construction

  @IT-1R5
  Rule: Reprocessing governed source evidence preserves identity

    @IT-1R5S1
    Scenario:  Reprocess a governed source artifact
      Given a governed source artifact already represented as REFS source evidence
      When the artifact is processed again
      Then its governed identity remains unchanged

    @IT-1R5S2
    Scenario:  Reprocessing does not duplicate source assertions
      Given assertions already extracted from a governed source artifact
      When the same artifact is processed again without source changes
      Then equivalent source assertions retain their governed identities
      And duplicate source assertions are not created