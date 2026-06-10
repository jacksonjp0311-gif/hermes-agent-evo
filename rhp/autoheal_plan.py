
# RHP-013.9 bounded autoheal plan generator.
from __future__ import annotations
import argparse, json
from dataclasses import dataclass, field
from typing import Any
from rhp.loop_registry import validate_loop

RHP_AUTOHEAL_PLAN_SCHEMA = "RHP-AUTOHEAL-PLAN-v0.1"

@dataclass(frozen=True)
class AutohealPlan:
    schema: str
    ok: bool
    classification: str
    repair_strategy: str
    loop: str
    attempt_budget: int
    allowed_paths: list[str] = field(default_factory=list)
    validation_commands: list[list[str]] = field(default_factory=list)
    evidence_outputs: list[str] = field(default_factory=list)
    mutation_allowed_now: bool = False
    commit_allowed_now: bool = False
    reason: str = ""
    non_claim_lock: str = (
        "Autoheal plans are plans only. They do not mutate files, execute repairs, commit, push, "
        "grant runtime/tool/CMS/memory/API/external-ingestion/autonomous/self-authorization authority, or bypass validation."
    )

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def plan_for_classification(classification: str, operation: str = "RHP") -> AutohealPlan:
    ok, failures = validate_loop("AUTOHEAL-PLAN", mutation_requested=False, commit_requested=False, attempt=1)
    if not ok:
        return AutohealPlan(RHP_AUTOHEAL_PLAN_SCHEMA, False, classification, "registry_rejected", "AUTOHEAL-PLAN", 0, reason=";".join(failures))

    if classification in {"dirty_worktree_and_module_path_execution_bug", "dirty_failed_attempt_residue"}:
        return AutohealPlan(
            RHP_AUTOHEAL_PLAN_SCHEMA, True, classification, "bounded_residue_cleanup_before_rebase",
            "AUTOHEAL-PLAN", 1,
            ["README.md", "AGENTS.md", "rhp/README.md", "rhp/autoheal_preflight.py", "rhp/autoheal_plan.py", "tests/test_rhp_013_9_*", "docs/context-layer/ops/RHP-013-9*"],
            [["python", "-m", "rhp.autoheal_preflight", "--operation", operation, "--json"]],
            ["docs/context-layer/ops/RHP-013-9-autoheal-preflight-box-plan-generator/autoheal-preflight-output.txt"],
            False, False, "Clean only bounded failed-attempt residue, verify clean, then pull/rebase."
        )

    if classification == "module_path_execution_bug":
        return AutohealPlan(
            RHP_AUTOHEAL_PLAN_SCHEMA, True, classification, "package_module_execution",
            "AUTOHEAL-PLAN", 1,
            ["AGENTS.md", "rhp/README.md", "docs/context-layer/ops/RHP-013-9*"],
            [["python", "-m", "rhp.resume_packet", "--repo-root", ".", "--json"]],
            ["docs/context-layer/ops/RHP-013-9-autoheal-preflight-box-plan-generator/module-execution-output.txt"],
            False, False, "Run package tools with python -m from repo root."
        )

    if classification == "tooling_escape_bug":
        return AutohealPlan(
            RHP_AUTOHEAL_PLAN_SCHEMA, True, classification, "escape_boundary_repair",
            "AUTOHEAL-PLAN", 1,
            ["rhp/*.py", "tests/test_rhp_*", "docs/context-layer/ops/RHP-013-9*"],
            [["python", "-m", "py_compile", "rhp/autoheal_preflight.py", "rhp/autoheal_plan.py"]],
            ["docs/context-layer/ops/RHP-013-9-autoheal-preflight-box-plan-generator/escape-repair-output.txt"],
            False, False, "Repair generated-code escaping errors and validate before mutation seal."
        )

    return AutohealPlan(
        RHP_AUTOHEAL_PLAN_SCHEMA, False, classification, "unknown_requires_diagnosis",
        "DIAGNOSIS", 0, reason="No bounded plan available for classification."
    )

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Generate bounded autoheal plan")
    p.add_argument("--classification", required=True)
    p.add_argument("--operation", default="RHP")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    plan = plan_for_classification(args.classification, args.operation)
    print(json.dumps(plan.as_dict(), indent=2, ensure_ascii=False))
    return 0 if plan.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
