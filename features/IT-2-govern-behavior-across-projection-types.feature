@IT-2
Feature: Govern behavior across projection types
  Projection behavior is governed by shared mapping knowledge and preferences.
  Applicable policy: REFS-Policy-on-JSON-and-JSON-LD-projections.md.
  Ordinary JSON and JSON-LD are distinct projection types under that policy.

  @IT-2R1
  Rule: A projects-to relationship identifies its source and target projections

    @IT-2R1S1
    Scenario: Relate one source projection to one target projection
      Given a source projection
      And a target projection
      When the source projection projects to the target projection
      Then the projects-to relationship identifies the source projection
      And the projects-to relationship identifies the target projection

    @IT-2R1S2
    Scenario: Preserve the direction of a projection
      Given a source projection
      And a target projection
      When the source projection projects to the target projection
      Then the source projection is distinguishable from the target projection
      And the projects-to relationship is directed from source to target

  @IT-2R2
  Rule: A projects-to relationship preserves required meaning

    @IT-2R2S1
    Scenario: Preserve a governed value across projections
      Given a source projection containing a governed value
      When the source projection projects to a target projection
      Then the target projection contains the governed value

    @IT-2R2S2
    Scenario: Preserve meaning across different projection types
      Given a source projection of one projection type
      And a target projection of a different projection type
      When the source projection projects to the target projection
      Then the required meaning of the source projection is preserved in the target projection

    @IT-2R2S3
    Scenario: Establish required meaning before approving a projection
      Given a projection request with an identified intended use
      And required meaning has not been established for that use
      When the request is evaluated
      Then the projection is not approved
      And the decision identifies the missing governed expectations

  @IT-2R3
  Rule: A projects-to relationship respects the expressive capabilities of its target projection

    @IT-2R3S1
    Scenario: Reject a target that cannot represent required meaning
      Given a source projection containing meaning required for the intended use
      And the target format and selected mapping conventions cannot represent that meaning
      When the projection request is evaluated
      Then the projection is rejected
      And the required meaning that cannot be represented is identified

    @IT-2R3S2
    Scenario: Preserve a concept through an explicit mapping convention
      Given an otherwise authorized projection request
      And the target format has no native representation for a required source concept
      And a governed mapping convention preserves that concept in the target
      When the source projects to the target using that convention
      Then the target preserves the required concept under the identified convention
      And the projection record identifies the convention needed to interpret it

    @IT-2R3S3
    Scenario: Reject a serialization that cannot preserve required named graphs
      Given a source RDF dataset whose named graph distinctions are required
      And the selected target serialization cannot represent those distinctions
      When the projection request is evaluated
      Then the projection is rejected
      And the decision identifies the unsupported named graph distinctions

  @IT-2R4
  Rule: Added, transformed, or omitted meaning is explicit and traceable

    @IT-2R4S1
    Scenario: Trace derived meaning to its supporting projection
      Given a source projection
      And applicable governed derivation rules and mapping preferences
      When the projection derives additional meaning in the target projection
      Then the additional meaning is identifiable as derived
      And the derivation is traceable to its supporting projection
      And the projection record identifies the rules and preferences applied

    @IT-2R4S2
    Scenario: Identify an explicit transformation of meaning
      Given a source projection
      And applicable governed transformation rules and mapping preferences
      When meaning is transformed while projecting to a target projection
      Then the transformation is explicitly identified
      And the transformed meaning is traceable to the source projection
      And the projection record identifies the rules and preferences applied

    @IT-2R4S3
    Scenario: Record a permitted omission of non-required meaning
      Given an otherwise authorized projection request
      And governed expectations permit omission of specified non-required meaning
      When the source projects to the target with that omission
      Then required meaning is preserved
      And the REFS projection record identifies the omitted meaning
      And the record retains the source references and expectations permitting the omission
      And the record is retained even if the receiver cannot accept it

  @IT-2R5
  Rule: Projection behavior is independent of the engine that executes it

    @IT-2R5S1
    Scenario: Produce equivalent governed results using different projection engines
      Given the same source projection
      And the same target projection type
      And the same governed expectations, mapping rules, and selected preferences
      When different projection engines perform the projection
      Then each resulting target satisfies the governed expectations
      And the results preserve equivalent required meaning

  @IT-2R6
  Rule: A projection result can be tested against its governed expectations

    @IT-2R6S1
    Scenario: Accept a target projection that satisfies its governed expectations
      Given a target projection that satisfies its governed expectations
      When the target projection is tested against those expectations
      Then the test result accepts the target projection

    @IT-2R6S2
    Scenario: Reject a target projection that violates its governed expectations
      Given a target projection that violates a governed expectation
      When the target projection is tested against its governed expectations
      Then the test result rejects the target projection
      And the violated expectation is identified

  @IT-2R7
  Rule: Ordinary JSON is permitted only for justified outbound integration

    @IT-2R7S1
    Scenario: Permit ordinary JSON for a receiver that requires it
      Given a specified device or external system requires ordinary JSON
      And no supported alternative meets the integration requirements
      And the request records the receiver, interface specification, and interface version
      And the request records why no supported alternative meets the requirement
      And the applicable mapping rules and conventions are identified
      And the projection can preserve the meaning required for its intended use
      And any proposed omission of non-required meaning is permitted and recorded
      When the projection request is evaluated
      Then the ordinary JSON target is permitted
      And the REFS projection record retains the justification
      And the record states that source reconstruction is not guaranteed
      And the record states that a reverse projection is not authorized

    @IT-2R7S2
    Scenario: Reject ordinary JSON selected for developer convenience
      Given a requested ordinary JSON target
      And a supported alternative meets the integration requirements
      And ordinary JSON was selected for developer convenience
      When the projection request is evaluated
      Then the ordinary JSON target is rejected
      And the decision identifies the last-resort target policy

    @IT-2R7S3
    Scenario: Withhold approval when the JSON justification is incomplete
      Given a requested ordinary JSON target
      And a required receiver, interface, justification, or mapping detail is missing
      When the projection request is evaluated
      Then the projection is not approved
      And the missing details are identified

    @IT-2R7S4
    Scenario: Review the justification when the receiving interface changes
      Given an ordinary JSON integration with a recorded justification
      When the receiving interface changes
      Then the justification is marked as requiring review
      And the review evaluates the changed interface requirements and supported alternatives

    @IT-2R7S5
    Scenario: Reject ordinary JSON as a source of governed knowledge
      Given a request to project ordinary JSON into REFS governed knowledge
      When the projection request is evaluated
      Then the projection is rejected
      And the decision identifies ordinary JSON knowledge sources as unsupported

    @IT-2R7S6
    Scenario: Read an operational response from an authorized integration
      Given an authorized integration returns an ordinary JSON acknowledgment or error response
      When REFS reads the response to determine the integration outcome
      Then the response may be processed as operational information
      And that processing does not itself admit the response as a source of governed knowledge

  @IT-2R8
  Rule: JSON-LD projections preserve governed RDF knowledge and interpretation

    @IT-2R8S1
    Scenario: Allow JSON-LD as a knowledge target
      Given a source containing a governed RDF graph or dataset
      And a requested JSON-LD target can preserve the required RDF knowledge
      And its required contexts and processing conventions satisfy governance requirements
      When the projection request is evaluated
      Then JSON-LD is allowed as a knowledge target
      And an ordinary JSON last-resort justification is not required

    @IT-2R8S2
    Scenario: Preserve the RDF knowledge required for the intended use
      Given an approved JSON-LD projection request
      When the source projects to JSON-LD
      Then the target preserves the required RDF graph or dataset
      And required resource identities, relationships, and literal datatypes are preserved

    @IT-2R8S3
    Scenario: Retain the knowledge needed to interpret JSON-LD
      Given an approved JSON-LD projection request
      When the source projects to JSON-LD
      Then required contexts, vocabulary identifiers, and processing conventions are identified
      And they are retained or resolvable through governed references

    @IT-2R8S4
    Scenario: Reject uncontrolled interpretation dependencies
      Given a requested JSON-LD projection
      And its interpretation depends on an undocumented assumption or an uncontrolled external context
      When the projection request is evaluated
      Then the projection is rejected
      And the uncontrolled interpretation dependency is identified

    @IT-2R8S5
    Scenario: Evaluate JSON-LD source admission separately
      Given JSON-LD is permitted as a target serialization
      And a JSON-LD source has not satisfied applicable source-governance requirements
      When admission of that source is evaluated
      Then target permission alone does not authorize source admission
      And the source is not admitted until those requirements are satisfied

  @IT-2R9
  Rule: Reversibility depends on preserving the same governed RDF knowledge

    @IT-2R9S1
    Scenario: Preserve an RDF graph through a serialization round trip
      Given governed RDF knowledge serialized as JSON-LD
      And another standardized serialization can preserve the same knowledge without loss
      And the conversions are authorized under applicable source-governance requirements
      When the knowledge is converted to that serialization and back to JSON-LD
      Then the resulting RDF graph is equivalent to the original graph
      And differences in formatting, property order, compact names, or layout do not invalidate equivalence

    @IT-2R9S2
    Scenario: Preserve named graphs through a dataset serialization round trip
      Given a governed RDF dataset containing required named graph distinctions
      And JSON-LD and another standardized dataset serialization can preserve that dataset
      And the conversions are authorized under applicable source-governance requirements
      When the dataset is converted between those serializations and back
      Then the resulting dataset is equivalent to the original dataset
      And the required named graph distinctions are preserved

  @IT-2R10
  Rule: A JSON transport envelope preserves the enclosed knowledge

    @IT-2R10S1
    Scenario: Treat an intact RDF document in JSON as transport
      Given an RDF document with a governed interpretation
      When the document is carried intact in a JSON transport envelope
      Then the envelope is treated as transport
      And source admission requirements apply to the enclosed RDF document
      And the enclosed knowledge retains its governed interpretation

    @IT-2R10S2
    Scenario: Reject an envelope that changes the enclosed knowledge
      Given a JSON envelope carrying an RDF document
      When transport verification detects altered, discarded, or ambiguously reinterpreted knowledge
      Then the envelope is rejected as a faithful transport of that document
      And the detected discrepancy is identified

  @IT-2R11
  Rule: Mapping preferences cannot override projection policy

    @IT-2R11S1
    Scenario: Reject a preference that conflicts with policy
      Given selected mapping preferences authorize an ordinary JSON knowledge source
      When the preferences are evaluated against projection policy
      Then the conflicting preferences are rejected
      And the conflicting policy requirement is identified
