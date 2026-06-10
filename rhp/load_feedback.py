# RHP-013.6 RHPLOAD Feedback Tree.
from __future__ import annotations
import argparse, json
from dataclasses import dataclass, field
from typing import Any

RHPLOAD_FEEDBACK_SCHEMA = "RHPLOAD-FEEDBACK-TREE-v0.1"

@dataclass(frozen=True)
class LoadFeedbackNode:
    label: str
    percent: int
    status: str = "pending"
    detail: str = ""
    children: list["LoadFeedbackNode"] = field(default_factory=list)
    def as_dict(self) -> dict[str, Any]:
        return {"label": self.label, "percent": self.percent, "status": self.status, "detail": self.detail, "children": [c.as_dict() for c in self.children]}

@dataclass(frozen=True)
class LoadFeedbackTree:
    ok: bool
    schema: str
    loop: str
    operation: str
    current_percent: int
    root: LoadFeedbackNode
    feedback: list[str] = field(default_factory=list)
    next_action: str = ""
    non_claim_lock: str = "RHPLOAD feedback trees are process state only. They grant no runtime, tool, CMS, memory, API, external-ingestion, autonomous, or self-authorization authority."
    def as_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "schema": self.schema, "loop": self.loop, "operation": self.operation, "current_percent": self.current_percent, "root": self.root.as_dict(), "feedback": list(self.feedback), "next_action": self.next_action, "non_claim_lock": self.non_claim_lock}

def render_tree(node: LoadFeedbackNode, prefix: str = "", is_last: bool = True) -> list[str]:
    branch = "`- " if is_last else "+- "
    line = f"{prefix}{branch}[{node.percent:03d}%] {node.label} | status={node.status}"
    if node.detail:
        line += f" | {node.detail}"
    lines = [line]
    child_prefix = prefix + ("   " if is_last else "|  ")
    for i, child in enumerate(node.children):
        lines.extend(render_tree(child, child_prefix, i == len(node.children) - 1))
    return lines

def build_standard_tree(loop: str, operation: str, current_percent: int, status: str = "running") -> LoadFeedbackTree:
    root = LoadFeedbackNode("All-One execution", current_percent, status, "expanded feedback tree", [
        LoadFeedbackNode("Rehydrate", 10, "ok", "repo root, branch, latest evidence"),
        LoadFeedbackNode("Select loop", 20, "ok", loop),
        LoadFeedbackNode("Inspect target surfaces", 35, status, "README, AGENTS, RHP evidence, tests"),
        LoadFeedbackNode("Mutate bounded surface", 60, "pending", "smallest valid patch"),
        LoadFeedbackNode("Validate", 80, "pending", "compile, focused tests, alignment guard"),
        LoadFeedbackNode("Seal", 90, "pending", "evidence, hashes, secret scan"),
        LoadFeedbackNode("Push and watch", 100, "pending", "commit, push, CI watch"),
    ])
    return LoadFeedbackTree(True, RHPLOAD_FEEDBACK_SCHEMA, loop, operation, current_percent, root, ["expanded tree supports zero-context handoff", "JSON mode supports machine resume"], "continue selected loop")

def render_feedback_tree(tree: LoadFeedbackTree) -> str:
    parts = [f"RHPLOAD [{tree.current_percent:03d}%] loop={tree.loop} operation={tree.operation}", "\n".join(render_tree(tree.root))]
    parts.extend([f"feedback: {x}" for x in tree.feedback])
    parts.append(f"next: {tree.next_action}")
    return "\n".join(parts)

def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--loop", default="DIAGNOSIS")
    p.add_argument("--operation", default="RHP")
    p.add_argument("--percent", type=int, default=0)
    p.add_argument("--status", default="running")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    tree = build_standard_tree(a.loop, a.operation, a.percent, a.status)
    print(json.dumps(tree.as_dict(), indent=2) if a.json else render_feedback_tree(tree))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
