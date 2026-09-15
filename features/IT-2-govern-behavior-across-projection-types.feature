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
      Then the required meaning of the source projection is preserved
      in the target projection

  @IT-2R3
  Rule: A projects-to relationship does not invent unsupported meaning

    @IT-2R3S1
    Scenario: Do not add unsupported meaning to a target projection
      Given a source projection
      When the source projection projects to a target projection
      Then every non-derived assertion added by the projection is supported
      by the source projection

  @IT-2R4
  Rule: Added or transformed meaning is explicit and traceable

    @IT-2R4S1
    Scenario: Trace derived meaning to its supporting projection
      Given a source projection
      When the projection derives additional meaning in the target projection
      Then the additional meaning is identifiable as derived
      And the derivation is traceable to its supporting projection

    @IT-2R4S2
    Scenario: Identify an explicit transformation of meaning
      Given a source projection
      When meaning is transformed while projecting to a target projection
      Then the transformation is explicitly identified
      And the transformed meaning is traceable to the source projection

  @IT-2R5
  Rule: Projection behavior is independent of the engine that executes it

    @IT-2R5S1
    Scenario: Produce equivalent governed results using different projection engines
      Given the same source projection
      And the same governed projection behavior
      When different projection engines perform the projection
      Then the resulting target projections satisfy the same governed expectations

  @IT-2R6
  Rule: A projection result can be tested against its governed expectations

    @IT-2R6S1
    Scenario: Accept a target projection that satisfies its governed expectations
      Given a target projection
      And governed expectations for that projection
      When the target projection is tested against those expectations
      Then the projection satisfies the governed expectations

    @IT-2R6S2
    Scenario: Reject a target projection that violates its governed expectations
      Given a target projection
      And governed expectations for that projection
      When the target projection violates those expectations
      Then the projection does not satisfy the governed expectations