from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

AuthorityTier = Literal["read_only", "diagnostic", "evidence_only", "authorized_mutation", "forbidden"]


@dataclass(frozen=True)
class LoopTool:
    name: str
    panel: str
    authority_tier: AuthorityTier
    purpose: str
    required_inputs: tuple[str, ...]
    writes_repo: bool
    closes_wound: bool
    repairs_code: bool
    grants_authority: bool


LOOP_TOOLS: tuple[LoopTool, ...] = (
    LoopTool(
        name="RHPZERO",
        panel="RHPZERO [GOLD]",
        authority_tier="read_only",
        purpose="Zero-context repository rehydration.",
        required_inputs=("README.md", "AGENTS.md", "latest-rhp.json", "latest evidence", "loop geometry"),
        writes_repo=False,
        closes_wound=False,
        repairs_code=False,
        grants_authority=False,
    ),
    LoopTool(
        name="RHPLOOP-GEOMETRY",
        panel="RHPLOOP-GEOMETRY [GOLD]",
        authority_tier="diagnostic",
        purpose="Validate live loop shape against sealed README/runtime geometry.",
        required_inputs=("README canonical run block", "rhp/loop_geometry.py"),
        writes_repo=False,
        closes_wound=False,
        repairs_code=False,
        grants_authority=False,
    ),
    LoopTool(
        name="RHPCI-CONNECTOR",
        panel="RHPCI-CONNECTOR [GOLD]",
        authority_tier="diagnostic",
        purpose="Classify GitHub connector CI observation before operator CI intake.",
        required_inputs=("subject commit", "combined status", "workflow runs"),
        writes_repo=False,
        closes_wound=False,
        repairs_code=False,
        grants_authority=False,
    ),
    LoopTool(
        name="RHPDIAG",
        panel="RHPDIAG",
        authority_tier="diagnostic",
        purpose="Render named failure class and raw artifact path.",
        required_inputs=("stage", "failure class", "raw artifact"),
        writes_repo=False,
        closes_wound=False,
        repairs_code=False,
        grants_authority=False,
    ),
    LoopTool(
        name="RHPDROP",
        panel="RHPDROP [closed]",
        authority_tier="evidence_only",
        purpose="Summarize command records and diagnostic-nonzero handling.",
        required_inputs=("command records", "raw outputs"),
        writes_repo=True,
        closes_wound=False,
        repairs_code=False,
        grants_authority=False,
    ),
    LoopTool(
        name="RHPREFLECT",
        panel="RHPREFLECT [GOLD]",
        authority_tier="evidence_only",
        purpose="Summarize what happened, what it means, and the next legal operation.",
        required_inputs=("latest state", "operation evidence", "active wound"),
        writes_repo=True,
        closes_wound=False,
        repairs_code=False,
        grants_authority=False,
    ),
    LoopTool(
        name="RHPSIM",
        panel="RHPSIM [GOLD]",
        authority_tier="read_only",
        purpose="Simulate a proposed loop transition before mutation.",
        required_inputs=("latest-rhp.json", "candidate operation class"),
        writes_repo=False,
        closes_wound=False,
        repairs_code=False,
        grants_authority=False,
    ),
    LoopTool(
        name="RHPHEAL",
        panel="RHPHEAL [PROPOSED]",
        authority_tier="diagnostic",
        purpose="Generate a no-execution repair proposal after failed logs are classified.",
        required_inputs=("wound packet", "failed logs", "bounded target files"),
        writes_repo=False,
        closes_wound=False,
        repairs_code=False,
        grants_authority=False,
    ),
)


def tool_names() -> tuple[str, ...]:
    return tuple(tool.name for tool in LOOP_TOOLS)


def get_tool(name: str) -> LoopTool:
    normalized = name.strip().upper()
    for tool in LOOP_TOOLS:
        if tool.name == normalized:
            return tool
    raise KeyError(normalized)


def tool_to_dict(tool: LoopTool) -> dict[str, Any]:
    return {
        "name": tool.name,
        "panel": tool.panel,
        "authority_tier": tool.authority_tier,
        "purpose": tool.purpose,
        "required_inputs": list(tool.required_inputs),
        "writes_repo": tool.writes_repo,
        "closes_wound": tool.closes_wound,
        "repairs_code": tool.repairs_code,
        "grants_authority": tool.grants_authority,
    }


def registry_to_dict() -> dict[str, Any]:
    return {
        "schema": "RHP-LOOP-TOOL-REGISTRY-v0.1",
        "tools": [tool_to_dict(tool) for tool in LOOP_TOOLS],
        "non_claim_lock": "Loop tools do not grant autonomous authority.",
    }


def forbidden_tools() -> tuple[str, ...]:
    return tuple(
        tool.name
        for tool in LOOP_TOOLS
        if tool.closes_wound or tool.repairs_code or tool.grants_authority
    )


def render_tool_registry_panel() -> str:
    lines = [
        "RHPTOOL [GOLD] status=registered",
        "`- loop tool registry",
        f"   +- total-tools: {len(LOOP_TOOLS)}",
        f"   +- read-only-tools: {sum(1 for t in LOOP_TOOLS if t.authority_tier == 'read_only')}",
        f"   +- diagnostic-tools: {sum(1 for t in LOOP_TOOLS if t.authority_tier == 'diagnostic')}",
        f"   +- evidence-only-tools: {sum(1 for t in LOOP_TOOLS if t.authority_tier == 'evidence_only')}",
        f"   +- forbidden-authority-tools: {len(forbidden_tools())}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
