from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from ..models.audit import AuditLog
from ..core.database import SessionLocal
import json


def write_audit_log(db: Session, action: str, ip: str, detail: str, user_id: Optional[int] = None) -> None:
    log = AuditLog(user_id=user_id, action=action, ip=ip, detail=detail)
    db.add(log)
    db.commit()


async def log_audit_event(action: str, details: Dict[str, Any], user_id: Optional[int] = None, ip_address: str = "127.0.0.1") -> None:
    """Async audit logging function"""
    db = SessionLocal()
    try:
        detail_str = json.dumps(details, ensure_ascii=False)
        log = AuditLog(
            user_id=user_id,
            action=action,
            ip=ip_address,
            detail=detail_str
        )
        db.add(log)
        db.commit()
        print(f"[AUDIT] {action}: {detail_str}")
    except Exception as e:
        print(f"[AUDIT ERROR] {action}: {str(e)}")
        db.rollback()
    finally:
        db.close()


