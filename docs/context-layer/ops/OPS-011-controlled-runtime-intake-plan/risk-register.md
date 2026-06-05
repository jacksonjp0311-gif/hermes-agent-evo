# OPS-011 Risk Register

| Risk | Why it matters | Control |
|---|---|---|
| Runtime jump | The system may try to move from seal directly to integration. | OPS-011 is planning only; OPS-012 must be read-only. |
| Memory write drift | Memory context may be mistaken for permission. | Authority matrix keeps memory_write=false. |
| CMS command drift | CMS evidence may be mistaken for command authority. | CMS remains read-only orientation. |
| Autonomy drift | "Online" may be misread as autonomous. | Online is defined as bounded, evidence-recorded, human-gated loop. |
| README drift | Post-seal path may advance without public state. | README must include the post-seal track before OPS-012. |

Non-claim lock: risk registration is not mitigation proof or production safety.
