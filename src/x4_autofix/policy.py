"""X4 autonomy policy enforcement."""
from __future__ import annotations
from enum import IntEnum


class AutonomyLevel(IntEnum):
    OBSERVE = 0
    ASSIST = 1
    GOVERNED = 2
    NEVER = 3


HARD_STOPS = {
    "delete_repository",
    "modify_secrets",
    "force_push_main",
    "change_visibility",
    "merge_without_review",
}


def may_apply(level: AutonomyLevel, action: str) -> bool:
    if action in HARD_STOPS:
        return False
    if level <= AutonomyLevel.OBSERVE:
        return False
    if level == AutonomyLevel.ASSIST:
        return action.startswith("propose_") or action == "open_pr"
    if level == AutonomyLevel.GOVERNED:
        return action in {"open_pr", "apply_lint_fix", "bump_action_version", "fix_typo"}
    return False
