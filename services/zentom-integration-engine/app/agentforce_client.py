"""
Zentom Integration Engine — Agentforce Client

Manages Agentforce (Salesforce autonomous agent) interactions for:
  - Executing approved actions in Salesforce
  - Managing action lifecycle (submit → approve → execute → verify)
  - Action type routing and validation
  - Rollback support for failed actions

Agentforce is Salesforce's autonomous agent platform. Zentom uses it
as the execution layer for approved remediation actions.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AgentforceActionType(str, Enum):
    UPDATE_RECORD = "update_record"
    DELETE_RECORD = "delete_record"
    CREATE_RECORD = "create_record"
    DISABLE_FLOW = "disable_flow"
    ENABLE_FLOW = "enable_flow"
    UPDATE_PERMISSION_SET = "update_permission_set"
    SEND_NOTIFICATION = "send_notification"
    RUN_DIAGNOSTIC = "run_diagnostic"
    RETRY_INTEGRATION = "retry_integration"
    CLEAR_CACHE = "clear_cache"
    DEPLOY_METADATA = "deploy_metadata"


class ActionStatus(str, Enum):
    SUBMITTED = "submitted"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    REJECTED = "rejected"


# Actions that require human approval before execution
HIGH_RISK_ACTIONS: set[str] = {
    AgentforceActionType.DELETE_RECORD.value,
    AgentforceActionType.DISABLE_FLOW.value,
    AgentforceActionType.UPDATE_PERMISSION_SET.value,
    AgentforceActionType.DEPLOY_METADATA.value,
}

# Actions that can be executed automatically
LOW_RISK_ACTIONS: set[str] = {
    AgentforceActionType.SEND_NOTIFICATION.value,
    AgentforceActionType.RUN_DIAGNOSTIC.value,
    AgentforceActionType.CLEAR_CACHE.value,
    AgentforceActionType.RETRY_INTEGRATION.value,
}


class AgentforceClient:
    """
    Agentforce API client for Zentom action execution.

    In production, this connects to Agentforce via:
      - Salesforce Agent API (Einstein AI Platform)
      - Flow Orchestration
      - Apex invocable actions

    In dev mode, returns simulated responses.
    """

    def __init__(
        self,
        endpoint_url: str = "",
        api_key: str = "",
        dev_mode: bool = True,
    ):
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.dev_mode = dev_mode
        self._action_counter = 0
        self._action_log: list[dict] = []

    def _next_action_id(self) -> str:
        """Generate a unique action ID."""
        self._action_counter += 1
        return f"af-act-{self._action_counter:06d}"

    def _is_high_risk(self, action_type: str) -> bool:
        """Check if an action type requires approval."""
        return action_type in HIGH_RISK_ACTIONS

    def submit_action(
        self,
        action_type: str,
        target_object: str = "",
        target_id: str = "",
        parameters: dict | None = None,
        org_id: str | None = None,
        incident_id: int | None = None,
        auto_approve: bool = False,
    ) -> dict:
        """
        Submit an action for execution.

        High-risk actions require approval before execution.
        Low-risk actions can be auto-approved if auto_approve is True.
        """
        action_id = self._next_action_id()

        # Validate action type
        valid_types = {a.value for a in AgentforceActionType}
        if action_type not in valid_types:
            return {
                "status": ActionStatus.REJECTED.value,
                "action_id": action_id,
                "error": f"Invalid action type: {action_type}",
            }

        # Determine if approval is needed
        requires_approval = self._is_high_risk(action_type)
        if requires_approval and not auto_approve:
            status = ActionStatus.PENDING_APPROVAL.value
        elif auto_approve and not requires_approval:
            status = ActionStatus.APPROVED.value
        else:
            status = ActionStatus.SUBMITTED.value

        action_record = {
            "action_id": action_id,
            "action_type": action_type,
            "target_object": target_object,
            "target_id": target_id,
            "parameters": parameters or {},
            "org_id": org_id,
            "incident_id": incident_id,
            "status": status,
            "requires_approval": requires_approval,
            "submitted_at": datetime.utcnow().isoformat(),
        }

        self._action_log.append(action_record)
        logger.info(f"Action {action_id} submitted: {action_type} → {status}")

        return action_record

    def approve_action(self, action_id: str, approver: str = "system") -> dict:
        """Approve a pending action for execution."""
        for action in self._action_log:
            if action["action_id"] == action_id:
                if action["status"] != ActionStatus.PENDING_APPROVAL.value:
                    return {
                        "status": "error",
                        "message": f"Action {action_id} is not pending approval (current: {action['status']})",
                    }
                action["status"] = ActionStatus.APPROVED.value
                action["approved_by"] = approver
                action["approved_at"] = datetime.utcnow().isoformat()
                return action

        return {"status": "error", "message": f"Action {action_id} not found"}

    def execute_action(self, action_id: str) -> dict:
        """
        Execute an approved action.

        In dev mode, simulates successful execution.
        In production, calls Agentforce API.
        """
        for action in self._action_log:
            if action["action_id"] == action_id:
                if action["status"] not in (ActionStatus.APPROVED.value, ActionStatus.SUBMITTED.value):
                    return {
                        "status": "error",
                        "message": f"Action {action_id} cannot be executed (current: {action['status']})",
                    }

                if self.dev_mode:
                    action["status"] = ActionStatus.COMPLETED.value
                    action["executed_at"] = datetime.utcnow().isoformat()
                    action["result"] = {
                        "success": True,
                        "message": f"Action {action['action_type']} executed successfully (simulated)",
                    }
                    logger.info(f"Action {action_id} executed: {action['action_type']}")
                    return action

                # Production: call Agentforce API
                return {"status": "not_implemented", "message": "Production Agentforce API not yet connected"}

        return {"status": "error", "message": f"Action {action_id} not found"}

    def reject_action(self, action_id: str, reason: str = "") -> dict:
        """Reject a pending action."""
        for action in self._action_log:
            if action["action_id"] == action_id:
                action["status"] = ActionStatus.REJECTED.value
                action["rejection_reason"] = reason
                action["rejected_at"] = datetime.utcnow().isoformat()
                return action

        return {"status": "error", "message": f"Action {action_id} not found"}

    def rollback_action(self, action_id: str) -> dict:
        """Attempt to rollback a completed action."""
        for action in self._action_log:
            if action["action_id"] == action_id:
                if action["status"] != ActionStatus.COMPLETED.value:
                    return {"status": "error", "message": "Only completed actions can be rolled back"}

                action["status"] = ActionStatus.ROLLED_BACK.value
                action["rolled_back_at"] = datetime.utcnow().isoformat()
                logger.warning(f"Action {action_id} rolled back: {action['action_type']}")
                return action

        return {"status": "error", "message": f"Action {action_id} not found"}

    def get_action(self, action_id: str) -> dict | None:
        """Get an action by ID."""
        for action in self._action_log:
            if action["action_id"] == action_id:
                return action
        return None

    def list_actions(
        self,
        status: str | None = None,
        action_type: str | None = None,
        limit: int = 50,
    ) -> list[dict]:
        """List actions with optional filters."""
        results = self._action_log
        if status:
            results = [a for a in results if a["status"] == status]
        if action_type:
            results = [a for a in results if a["action_type"] == action_type]
        return results[-limit:]

    def get_stats(self) -> dict:
        """Get action statistics."""
        total = len(self._action_log)
        by_status = {}
        for action in self._action_log:
            s = action["status"]
            by_status[s] = by_status.get(s, 0) + 1

        return {
            "total_actions": total,
            "by_status": by_status,
            "high_risk_types": list(HIGH_RISK_ACTIONS),
            "low_risk_types": list(LOW_RISK_ACTIONS),
        }


# Global client instance
_client: AgentforceClient | None = None


def get_client(dev_mode: bool = True) -> AgentforceClient:
    """Get or create the global AgentforceClient instance."""
    global _client
    if _client is None:
        _client = AgentforceClient(dev_mode=dev_mode)
    return _client


def execute_agentforce_action(action: dict) -> dict:
    """
    Backward-compatible function to execute an Agentforce action.

    Args:
        action: Dict with action_type, target_object, target_id, parameters, etc.
    """
    client = get_client()
    result = client.submit_action(
        action_type=action.get("action_type", "send_notification"),
        target_object=action.get("target_object", ""),
        target_id=action.get("target_id", ""),
        parameters=action.get("parameters"),
        org_id=action.get("org_id"),
        incident_id=action.get("incident_id"),
        auto_approve=action.get("auto_approve", False),
    )

    # If auto-approved or low-risk, execute immediately
    if result.get("status") in (ActionStatus.APPROVED.value, ActionStatus.SUBMITTED.value):
        exec_result = client.execute_action(result["action_id"])
        return exec_result

    return result

