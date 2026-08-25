#!/usr/bin/env python3
from __future__ import annotations


VALID_STATES = {
    "STAGED",
    "APPROVED",
    "REJECTED",
    "COMMITTED",
}

ALLOWED_TRANSITIONS = {
    "STAGED": {"APPROVED", "REJECTED"},
    "APPROVED": {"COMMITTED"},
    "REJECTED": set(),
    "COMMITTED": set(),
}


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


def can_transition(current: str, target: str) -> bool:
    if current not in ALLOWED_TRANSITIONS:
        return False
    return target in ALLOWED_TRANSITIONS[current]