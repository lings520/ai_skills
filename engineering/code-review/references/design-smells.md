# Maintainability heuristics

Use these Fowler-inspired heuristics only when they identify a consequential problem in the selected changes. They are judgment calls, not mandatory violations or instructions to refactor. A documented repository convention takes precedence.

| Possible smell | Look for | Potential direction |
| --- | --- | --- |
| Mysterious Name | Names obscure a meaningful responsibility or invariant | Use terminology that makes the responsibility clear |
| Duplicated Code | Repeated logic will require coordinated corrections | Share the genuinely common behaviour |
| Feature Envy | Behaviour depends mostly on another module's data | Reconsider where that behaviour belongs |
| Data Clumps | The same related values repeatedly travel together | Consider a cohesive value/type |
| Primitive Obsession | Raw values conceal important domain constraints | Represent the constraints explicitly |
| Repeated Switches | Multiple sites duplicate the same variant dispatch | Consolidate dispatch where that reduces maintenance |
| Shotgun Surgery | One behavioural change requires scattered edits | Bring related responsibilities together |
| Divergent Change | One module mixes unrelated reasons to change | Separate responsibilities where justified |
| Speculative Generality | Hooks and abstractions serve no current requirement | Simplify to the supported use cases |
| Message Chains | Callers depend on hidden navigation structure | Expose the behaviour they actually need |
| Middle Man | Delegation adds no useful policy or isolation | Consider removing unnecessary indirection |
| Refused Bequest | Inherited contracts are largely rejected or bypassed | Reconsider the relationship or use composition |

Explain the concrete maintenance cost before suggesting a change. Do not flag deliberate adapters, framework conventions, or coincidentally similar code solely because they resemble a smell. Security and functional defects take precedence over stylistic preferences.
