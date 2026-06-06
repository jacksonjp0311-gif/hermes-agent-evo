# OPS-025 Read-Only Context Injection into Hermes Proposal Path

- operation: OPS-025
- read-only context injection into proposal path passed: true
- runtime source mutation: true
- default behavior changed: false
- environment gate: `HERMES_HRCN_CONTEXT`
- focused tests passed: true
- direct context injection smoke passed: true
- test expectation repair used: true
- CMS write: false
- memory write: false
- API write: false
- provider/model call executed: false
- tool use executed: false
- autonomous authority: false
- self-authorization: false

## Use

Set `HERMES_HRCN_CONTEXT=1` to append read-only HRCN orientation to the ephemeral system prompt.

## Non-Claim Lock

OPS-025 is not CMS execution, not CMS write, not memory write, not API write, not provider/model execution, not tool authority, not autonomy, and not self-authorization.
