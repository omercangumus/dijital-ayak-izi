from typing import Optional
from sqlalchemy.orm import Session
from ..models.audit import AuditLog


def write_audit_log(db: Session, action: str, ip: str, detail: str, user_id: Optional[int] = None) -> None:
    log = AuditLog(user_id=user_id, action=action, ip=ip, detail=detail)
    db.add(log)
    db.commit()


