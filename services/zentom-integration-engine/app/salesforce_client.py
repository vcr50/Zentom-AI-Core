"""
Zentom Integration Engine — Salesforce Client

Manages Salesforce API interactions for:
  - Publishing cases and tasks from incidents
  - Querying org health and object metadata
  - Creating incident records (Sentinel_Incident__c)
  - Updating record statuses

Supports both connected app (OAuth) and session-based auth.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)


class SalesforceAuthType(str, Enum):
    OAUTH = "oauth"
    SESSION = "session"
    API_TOKEN = "api_token"


class SalesforceOperation(str, Enum):
    CREATE_CASE = "create_case"
    CREATE_TASK = "create_task"
    CREATE_INCIDENT = "create_incident"
    UPDATE_RECORD = "update_record"
    QUERY = "query"
    DESCRIBE = "describe"


class SalesforceClient:
    """
    Salesforce API client for Zentom integrations.

    In production, this connects to Salesforce via:
      - Connected App (OAuth 2.0 JWT Bearer flow)
      - Session ID from Apex context
      - API token for external integrations

    In dev mode, returns simulated responses.
    """

    def __init__(
        self,
        instance_url: str = "",
        access_token: str = "",
        api_version: str = "62.0",
        dev_mode: bool = True,
    ):
        self.instance_url = instance_url
        self.access_token = access_token
        self.api_version = api_version
        self.dev_mode = dev_mode
        self._call_count = 0

    @property
    def is_configured(self) -> bool:
        """Check if the client has valid credentials."""
        return bool(self.instance_url and self.access_token) or self.dev_mode

    def _next_id(self) -> str:
        """Generate a mock Salesforce ID."""
        self._call_count += 1
        return f"500{self._call_count:010d}"

    def _headers(self) -> dict:
        """Build request headers."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _rest_url(self, path: str) -> str:
        """Build REST API URL."""
        return f"{self.instance_url}/services/data/v{self.api_version}/{path}"

    # -----------------------------------------------------------------------
    # Case Management
    # -----------------------------------------------------------------------

    def create_case(
        self,
        subject: str,
        description: str = "",
        origin: str = "Zentom AI",
        priority: str = "Medium",
        org_id: str | None = None,
    ) -> dict:
        """
        Create a Salesforce Case from an incident.

        Returns the case ID and status.
        """
        if not self.is_configured:
            return {"status": "not_configured", "error": "Salesforce credentials not set"}

        if self.dev_mode:
            case_id = self._next_id()
            logger.info(f"[DEV] Created Case {case_id}: {subject}")
            return {
                "status": "created",
                "case_id": case_id,
                "subject": subject,
                "origin": origin,
                "priority": priority,
                "org_id": org_id,
            }

        # Production: POST to /services/data/v62.0/sobjects/Case
        # Placeholder for actual HTTP call
        return {"status": "not_implemented", "message": "Production Salesforce API not yet connected"}

    def create_task(
        self,
        what_id: str,
        subject: str,
        description: str = "",
        owner_id: str | None = None,
        priority: str = "Normal",
    ) -> dict:
        """
        Create a Salesforce Task linked to a Case or Incident.

        Args:
            what_id: ID of the parent record (Case, Incident, etc.)
            subject: Task subject line
            description: Task body
            owner_id: Assigned user ID
            priority: High, Normal, Low
        """
        if not self.is_configured:
            return {"status": "not_configured", "error": "Salesforce credentials not set"}

        if self.dev_mode:
            task_id = f"00T{self._call_count:010d}"
            self._call_count += 1
            return {
                "status": "created",
                "task_id": task_id,
                "what_id": what_id,
                "subject": subject,
                "priority": priority,
            }

        return {"status": "not_implemented", "message": "Production Salesforce API not yet connected"}

    # -----------------------------------------------------------------------
    # Sentinel Incident Custom Object
    # -----------------------------------------------------------------------

    def create_incident_record(
        self,
        incident_type: str,
        severity: str = "Medium",
        error_message: str = "",
        org_id: str | None = None,
        environment: str = "sandbox",
        raw_payload: dict | None = None,
    ) -> dict:
        """
        Create a Sentinel_Incident__c custom object record.

        This is the primary way Zentom logs incidents in Salesforce.
        """
        if not self.is_configured:
            return {"status": "not_configured", "error": "Salesforce credentials not set"}

        if self.dev_mode:
            record_id = f"a1{self._call_count:011d}"
            self._call_count += 1
            return {
                "status": "created",
                "record_id": record_id,
                "incident_type": incident_type,
                "severity": severity,
                "org_id": org_id,
                "environment": environment,
            }

        return {"status": "not_implemented", "message": "Production Salesforce API not yet connected"}

    def update_incident_status(
        self,
        record_id: str,
        status: str,
        resolution_notes: str = "",
    ) -> dict:
        """Update the status of a Sentinel_Incident__c record."""
        if self.dev_mode:
            return {
                "status": "updated",
                "record_id": record_id,
                "new_status": status,
                "resolution_notes": resolution_notes,
            }

        return {"status": "not_implemented", "message": "Production Salesforce API not yet connected"}

    # -----------------------------------------------------------------------
    # Query Operations
    # -----------------------------------------------------------------------

    def query(self, soql: str) -> dict:
        """
        Execute a SOQL query.

        Args:
            soql: SOQL query string
        """
        if not self.is_configured:
            return {"status": "not_configured", "error": "Salesforce credentials not set"}

        if self.dev_mode:
            return {
                "status": "success",
                "total_size": 0,
                "records": [],
                "soql": soql,
            }

        return {"status": "not_implemented", "message": "Production Salesforce API not yet connected"}

    def get_org_health(self, org_id: str) -> dict:
        """
        Get organization health metrics.

        Queries API usage, storage, and active users.
        """
        if self.dev_mode:
            return {
                "org_id": org_id,
                "api_usage_percent": 23,
                "storage_usage_percent": 45,
                "active_users": 142,
                "health_score": 87,
                "status": "healthy",
            }

        return {"status": "not_implemented", "message": "Production Salesforce API not yet connected"}


# Global client instance
_client: SalesforceClient | None = None


def get_client(
    instance_url: str = "",
    access_token: str = "",
    dev_mode: bool = True,
) -> SalesforceClient:
    """Get or create the global SalesforceClient instance."""
    global _client
    if _client is None:
        _client = SalesforceClient(
            instance_url=instance_url,
            access_token=access_token,
            dev_mode=dev_mode,
        )
    return _client


def publish_salesforce_case(payload: dict) -> dict:
    """
    Backward-compatible function to publish a Salesforce Case.

    Args:
        payload: Dict with subject, description, origin, priority, org_id
    """
    client = get_client()
    return client.create_case(
        subject=payload.get("subject", "Zentom Incident"),
        description=payload.get("description", ""),
        origin=payload.get("origin", "Zentom AI"),
        priority=payload.get("priority", "Medium"),
        org_id=payload.get("org_id"),
    )

