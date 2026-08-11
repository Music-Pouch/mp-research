# Research runner architecture

```text
Research brief / GitHub spike
          |
          v
     mp-research CLI
          |
          v
   ResearchAdapter
    /     |      \
   /      |       \
GPTR     ODR      STORM
   \      |       /
    \     |      /
          v
  EvidenceBundle v0.1
          |
      +---+---+
      |       |
 evidence  report
  .json     .md
      |
 evaluation harness
      |
 ADR candidate / durable research / implementation work
```

## Invariants

1. The evidence schema belongs to Music Pouch.
2. Native engine output is preserved before normalization.
3. Missing provenance stays missing; the adapter does not fabricate it.
4. Engine selection is explicit until RS-002 provides evidence for routing.
5. Research engines do not accept ADRs.
6. The GitHub issue -> brief -> evidence bundle flow stays stable across provider changes.
7. The default runnable path should stay available without paid credits wherever practical.
8. Paid providers are extensions, not prerequisites.
