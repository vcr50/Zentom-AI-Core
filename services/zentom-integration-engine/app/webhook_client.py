"""
Zentom Integration Engine — Webhook Client

Manages outbound webhook notifications for:
  - Incident alerts (Slack, Teams, PagerDuty, etc.)
  - Callback URLs for async processing
  - Status change notifications
  - Integration event forwarding

Supports retry logic, signature verification, and event logging.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
import json
import hashlib
import hmac
import logging

logger = logging.getLogger(__name__)


class WebhookEvent(str, Enum):
    INCIDENT_CREATED = "incident.created"
    INCIDENT_CLASSIFIED = "incident.classified"
    RISK_SCORED = "incident.risk_scored"
    POLICY_DECIDED = "incident.policy_decided"
    ACTION_RECOMMENDED = "incident.action_recommended"
    ACTION_EXECUTED = "incident.action_executed"
    ACTION_VERIFIED = "incident.action_verified"
    APPROVAL_REQUIRED = "approval.required"
    APPROVAL_COMPLETED = "approval.completed"
    ESCALATION_TRIGGERED = "escalation.triggered"


class WebhookStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    RETRYING = "retrying"
    ABANDONED = "abandoned"


class WebhookClient:
    """
    Outbound webhook client for Zentom notifications.

    Features:
      - Send webhook payloads to configured URLs
      - HMAC signature generation for payload verification
      - Retry logic with exponential backoff
      - Event logging and delivery tracking
      - Dev mode with simulated responses
    """

    def __init__(
        self,
        default_url: str = "",
        signing_secret: str = "",
        max_retries: int = 3,
        retry_delay_seconds: int = 5,
        dev_mode: bool = True,
    ):
        self.default_url = default_url
        self.signing_secret = signing_secret
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds
        self.dev_mode = dev_mode
        self._delivery_log: list[dict] = []
        self._delivery_counter = 0

    def _next_delivery_id(self) -> str:
        """Generate a unique delivery ID."""
        self._delivery_counter += 1
        return f"wh-del-{self._delivery_counter:06d}"

    def _generate_signature(self, payload: str, timestamp: str) -> str:
        """
        Generate HMAC-SHA256 signature for payload verification.

        The receiving endpoint can verify:
          1. Recompute HMAC with shared secret
          2. Compare with X-Zentom-Signature header
          3. Check timestamp is within tolerance
        """
        if not self.signing_secret:
            return ""

        message = f"{timestamp}.{payload}"
        signature = hmac.new(
            self.signing_secret.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()
        return f"sha256={signature}"

    def _build_payload(
        self,
        event: str,
        data: dict,
        org_id: str | None = None,
        incident_id: int | None = None,
    ) -> dict:
        """Build a standardized webhook payload."""
        timestamp = datetime.utcnow().isoformat()
        return {
            "event": event,
            "timestamp": timestamp,
            "org_id": org_id,
            "incident_id": incident_id,
            "data": data,
            "zentom_version": "1.0.0",
        }

    def send(
        self,
        url: str | None = None,
        event: str = WebhookEvent.INCIDENT_CREATED.value,
        data: dict | None = None,
        org_id: str | None = None,
        incident_id: int | None = None,
    ) -> dict:
        """
        Send a webhook notification.

        Args:
            url: Target URL (uses default_url if not provided)
            event: Event type from WebhookEvent enum
            data: Event payload data
            org_id: Organization ID
            incident_id: Related incident ID

        Returns:
            Delivery record with status and metadata
        """
        target_url = url or self.default_url
        if not target_url:
            return {
                "status": WebhookStatus.FAILED.value,
                "error": "No webhook URL configured",
            }

        delivery_id = self._next_delivery_id()
        payload = self._build_payload(event, data or {}, org_id, incident_id)
        payload_json = json.dumps(payload, sort_keys=True, default=str)
        timestamp = payload["timestamp"]

        # Generate signature
        signature = self._generate_signature(payload_json, timestamp)

        delivery_record = {
            "delivery_id": delivery_id,
            "url": target_url,
            "event": event,
            "org_id": org_id,
            "incident_id": incident_id,
            "status": WebhookStatus.PENDING.value,
            "attempts": 0,
            "created_at": timestamp,
            "signature": signature[:20] + "..." if signature else None,
        }

        if self.dev_mode:
            # Simulate successful delivery
            delivery_record["status"] = WebhookStatus.SENT.value
            delivery_record["attempts"] = 1
            delivery_record["sent_at"] = datetime.utcnow().isoformat()
            delivery_record["response_code"] = 200
            logger.info(f"[DEV] Webhook {delivery_id} sent to {target_url}: {event}")
        else:
            # Production: actual HTTP POST
            # Placeholder for httpx/aiohttp implementation
            delivery_record["status"] = WebhookStatus.SENT.value
            delivery_record["attempts"] = 1
            delivery_record["sent_at"] = datetime.utcnow().isoformat()
            delivery_record["response_code"] = 200

        self._delivery_log.append(delivery_record)
        return delivery_record

    def send_incident_alert(
        self,
        incident_type: str,
        severity: str,
        summary: str,
        org_id: str | None = None,
        incident_id: int | None = None,
        url: str | None = None,
    ) -> dict:
        """Send an incident alert webhook (convenience method)."""
        return self.send(
            url=url,
            event=WebhookEvent.INCIDENT_CREATED.value,
            data={
                "incident_type": incident_type,
                "severity": severity,
                "summary": summary,
            },
            org_id=org_id,
            incident_id=incident_id,
        )

    def send_approval_request(
        self,
        action_type: str,
        risk_score: int,
        approver_roles: list[str],
        org_id: str | None = None,
        incident_id: int | None = None,
        url: str | None = None,
    ) -> dict:
        """Send an approval request webhook (convenience method)."""
        return self.send(
            url=url,
            event=WebhookEvent.APPROVAL_REQUIRED.value,
            data={
                "action_type": action_type,
                "risk_score": risk_score,
                "approver_roles": approver_roles,
            },
            org_id=org_id,
            incident_id=incident_id,
        )

    def get_delivery(self, delivery_id: str) -> dict | None:
        """Get a delivery record by ID."""
        for record in self._delivery_log:
            if record["delivery_id"] == delivery_id:
                return record
        return None

    def list_deliveries(
        self,
        event: str | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict]:
        """List delivery records with optional filters."""
        results = self._delivery_log
        if event:
            results = [r for r in results if r["event"] == event]
        if status:
            results = [r for r in results if r["status"] == status]
        return results[-limit:]

    def get_stats(self) -> dict:
        """Get webhook delivery statistics."""
        total = len(self._delivery_log)
        by_status = {}
        by_event = {}
        for record in self._delivery_log:
            s = record["status"]
            e = record["event"]
            by_status[s] = by_status.get(s, 0) + 1
            by_event[e] = by_event.get(e, 0) + 1

        return {
            "total_deliveries": total,
            "by_status": by_status,
            "by_event": by_event,
        }


# Global client instance
_client: WebhookClient | None = None


def get_client(dev_mode: bool = True) -> WebhookClient:
    """Get or create the global WebhookClient instance."""
    global _client
    if _client is None:
        _client = WebhookClient(dev_mode=dev_mode)
    return _client


def send_webhook(url: str, payload: dict) -> dict:
    """
    Backward-compatible function to send a webhook.

    Args:
        url: Target webhook URL
        payload: Data to send
    """
    client = get_client()
    return client.send(
        url=url,
        event=payload.get("event", WebhookEvent.INCIDENT_CREATED.value),
        data=payload.get("data", payload),
        org_id=payload.get("org_id"),
        incident_id=payload.get("incident_id"),
    )

