# CMS Task Routing Matrix

| Change type | Read first | Validate |
|---|---|---|
| Runtime patch | `src/cms/README.md`, `src/cms/core/README.md`, `tests/` | compile + import + unit tests |
| Metric patch | `src/cms/metrics/README.md` | architecture validator + tests |
| Feedback patch | `src/cms/feedback/README.md` | runtime cycle + feedback tests |
| Memory patch | `src/cms/memory/README.md` | memory tests + non-claim review |
| RCC patch | `README.md`, `docs/context/`, `rcc/nexus/` | `python scripts/rcc/check_rcc_nexus.py` |
| README patch | root and target mini README | `python scripts/rcc/audit_readme_surface.py` |
| Architecture patch | `docs/architecture/`, `docs/protocols/` | `python scripts/validation/validate_architecture_contracts.py` |
| Release patch | `docs/release_seals/`, `reports/release/` | release validator |

| Thread rehydration | `docs/context/THREAD_REHYDRATION_PROTOCOL.md`, `outputs/version_registry/cms_version_registry.json`, latest validation reports | thread rehydration validation + README audit |
