# RHP Autoheal Executor Dry-Run

Schema: `RHP-AUTOHEAL-EXECUTOR-DRY-RUN-v0.1`
Operation: `RHP-015.0`
CI status: `red`
Autoheal execution enabled: `False`
Dry-run only: `True`

| Step | Mode | Allowed | Executes |
|---|---|---:|---:|
| collect_ci_wound | `read_or_paste_only` | `True` | `False` |
| classify_failure | `diagnosis_only` | `True` | `False` |
| propose_patch | `proposal_only` | `True` | `False` |
| execute_patch | `blocked` | `False` | `False` |
| rerun_ci | `blocked` | `False` | `False` |

Recommendation: Collect remote CI logs or copied failure text next; keep execution disabled until the dry-run plan is reviewed.

Non-claim lock: Autoheal dry-run proposes and classifies only. It does not mutate files, execute repairs, rerun CI, or grant authority.
