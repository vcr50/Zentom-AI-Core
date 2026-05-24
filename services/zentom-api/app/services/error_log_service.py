import logging

from sqlalchemy.orm import Session

from app.models import ApiErrorLog

logger = logging.getLogger(__name__)


def log_api_error(
    db: Session,
    *,
    path: str,
    method: str,
    status_code: int,
    error_type: str,
    error_message: str,
    payload: dict | None = None,
    client_host: str | None = None,
) -> None:
    payload = payload or {}

    try:
        db.rollback()
        db.add(
            ApiErrorLog(
                path=path,
                method=method,
                status_code=status_code,
                error_type=error_type,
                error_message=error_message,
                org_id=payload.get("orgId"),
                incident_type=payload.get("incidentType"),
                source=payload.get("source"),
                client_host=client_host,
            )
        )
        db.commit()
    except Exception as exc:
        db.rollback()
        logger.warning("API error logging failed: %s", exc)
