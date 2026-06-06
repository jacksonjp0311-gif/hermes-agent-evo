# OPS-023 Wire Read-Only Bridge Status

- operation: OPS-023
- read-only bridge status wired: true
- status commands: `hermes hrcn status`, `hermes hrcn-status`
- optional startup display: `HERMES_HRCN_BRIDGE=1`
- default startup behavior changed: false
- focused tests passed: true
- status command smoke passed: true
- CMS write: false
- memory write: false
- API write: false
- provider/model call executed: false
- tool use executed: false
- autonomous authority: false
- self-authorization: false

## Non-Claim Lock

OPS-023 exposes read-only status only. It is not CMS execution, not CMS write, not memory write, not API write, not provider/model execution, not tool authority, not autonomy, and not self-authorization.
