"""Simulated core banking action service with risk-tiered approvals and immutable audit trail."""
from datetime import datetime
from typing import Any


class ActionService:
    """Manages case creation, entity flags, account freezes, and approval lifecycles."""

    def __init__(self):
        self.cases: dict[str, dict[str, Any]] = {}
        self.action_log: list[dict[str, Any]] = []
        self.actions_by_id: dict[str, dict[str, Any]] = {}
        self.idempotency_cache: dict[str, dict[str, Any]] = {}
        self.frozen_accounts: set[str] = set()
        self.blocked_devices: set[str] = set()
        self.flagged_entities: set[str] = set()
        self._action_counter = 1000
        self._case_counter = 2000

    def create_case(self, title: str, entity_ids: list[str], summary: str) -> str:
        """Opens an investigation case linking involved entities."""
        self._case_counter += 1
        case_id = f"CASE-{self._case_counter}"
        self.cases[case_id] = {
            "case_id": case_id,
            "title": title,
            "entity_ids": entity_ids,
            "summary": summary,
            "status": "OPEN",
            "created_at": datetime.now().isoformat()
        }
        return case_id

    def flag_entity(
        self,
        case_id: str,
        entity_id: str,
        reason: str,
        evidence_ids: list[str],
        idempotency_key: str | None = None
    ) -> dict[str, Any]:
        """Flags an entity as suspicious (Auto-executed)."""
        if idempotency_key and idempotency_key in self.idempotency_cache:
            return self.idempotency_cache[idempotency_key]

        self._action_counter += 1
        action_id = f"ACT-{self._action_counter}"
        self.flagged_entities.add(entity_id)

        record = {
            "action_id": action_id,
            "case_id": case_id,
            "action_type": "FLAG_ENTITY",
            "target_id": entity_id,
            "status": "AUTO_EXECUTED",
            "reason": reason,
            "evidence_ids": evidence_ids or [],
            "approver": "SYSTEM",
            "timestamp": datetime.now().isoformat(),
            "reversed": False
        }

        self.action_log.append(record)
        self.actions_by_id[action_id] = record
        if idempotency_key:
            self.idempotency_cache[idempotency_key] = record

        return record

    def freeze_account(
        self,
        case_id: str,
        account_id: str,
        reason: str,
        evidence_ids: list[str],
        auto_exec: bool = False,
        idempotency_key: str | None = None
    ) -> dict[str, Any]:
        if idempotency_key and idempotency_key in self.idempotency_cache:
            return self.idempotency_cache[idempotency_key]

        # Check blast radius: no more than 10 freeze actions per case
        existing_freezes = [
            a for a in self.action_log
            if a.get("case_id") == case_id and a.get("action_type") == "FREEZE_ACCOUNT"
        ]
        if len(existing_freezes) >= 10:
            raise ValueError(
                f"Blast radius limit exceeded: Maximum 10 account freezes allowed per case (case '{case_id}' already has {len(existing_freezes)})"
            )

        self._action_counter += 1
        action_id = f"ACT-{self._action_counter}"
        status = "APPROVED" if auto_exec else "PENDING_APPROVAL"
        approver = "SYSTEM" if auto_exec else None

        if auto_exec:
            self.frozen_accounts.add(account_id)

        record = {
            "action_id": action_id,
            "case_id": case_id,
            "action_type": "FREEZE_ACCOUNT",
            "target_id": account_id,
            "status": status,
            "reason": reason,
            "evidence_ids": evidence_ids or [],
            "approver": approver,
            "timestamp": datetime.now().isoformat(),
            "reversed": False
        }

        self.action_log.append(record)
        self.actions_by_id[action_id] = record
        if idempotency_key:
            self.idempotency_cache[idempotency_key] = record

        return record

    def block_device(
        self,
        case_id: str,
        device_id: str,
        reason: str,
        evidence_ids: list[str],
        idempotency_key: str | None = None
    ) -> dict[str, Any]:
        """Queues a device block for review."""
        if idempotency_key and idempotency_key in self.idempotency_cache:
            return self.idempotency_cache[idempotency_key]

        self._action_counter += 1
        action_id = f"ACT-{self._action_counter}"

        record = {
            "action_id": action_id,
            "case_id": case_id,
            "action_type": "BLOCK_DEVICE",
            "target_id": device_id,
            "status": "PENDING_APPROVAL",
            "reason": reason,
            "evidence_ids": evidence_ids or [],
            "approver": None,
            "timestamp": datetime.now().isoformat(),
            "reversed": False
        }

        self.action_log.append(record)
        self.actions_by_id[action_id] = record
        if idempotency_key:
            self.idempotency_cache[idempotency_key] = record

        return record

    def approve_action(self, action_id: str, approver_id: str) -> dict[str, Any]:
        """Approves and executes a pending action."""
        if action_id not in self.actions_by_id:
            raise ValueError(f"Action '{action_id}' not found")

        record = self.actions_by_id[action_id]
        if record["status"] != "PENDING_APPROVAL":
            raise ValueError(f"Action '{action_id}' is not in PENDING_APPROVAL status (currently {record['status']})")

        record["status"] = "APPROVED"
        record["approver"] = approver_id
        record["approved_at"] = datetime.now().isoformat()

        # Apply state effect
        if record["action_type"] == "FREEZE_ACCOUNT":
            self.frozen_accounts.add(record["target_id"])
        elif record["action_type"] == "BLOCK_DEVICE":
            self.blocked_devices.add(record["target_id"])

        return record

    def reverse_action(self, action_id: str, reason: str, approver_id: str) -> dict[str, Any]:
        """Reverses an executed action (e.g. unfreeze, unflag)."""
        if action_id not in self.actions_by_id:
            raise ValueError(f"Action '{action_id}' not found")

        record = self.actions_by_id[action_id]
        record["status"] = "REVERSED"
        record["reversed"] = True
        record["reversal_reason"] = reason
        record["reversal_approver"] = approver_id
        record["reversed_at"] = datetime.now().isoformat()

        # Undo state effect
        if record["action_type"] == "FREEZE_ACCOUNT":
            self.frozen_accounts.discard(record["target_id"])
        elif record["action_type"] == "BLOCK_DEVICE":
            self.blocked_devices.discard(record["target_id"])
        elif record["action_type"] == "FLAG_ENTITY":
            self.flagged_entities.discard(record["target_id"])

        return record

    def is_account_frozen(self, account_id: str) -> bool:
        """Returns True if the account is currently frozen."""
        return account_id in self.frozen_accounts

    def is_device_blocked(self, device_id: str) -> bool:
        """Returns True if the device is currently blocked."""
        return device_id in self.blocked_devices

    def get_action_log(self, case_id: str | None = None) -> list[dict[str, Any]]:
        """Returns immutable action audit log entries."""
        if case_id:
            return [a for a in self.action_log if a.get("case_id") == case_id]
        return list(self.action_log)
