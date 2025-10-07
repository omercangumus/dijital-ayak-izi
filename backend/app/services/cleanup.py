from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..models.audit import AuditLog


def cleanup_old_data(days: int = 30):
    db = SessionLocal()
    try:
        threshold = datetime.utcnow() - timedelta(days=days)
        db.query(AuditLog).filter(AuditLog.created_at < threshold).delete()
        db.commit()
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_old_data, "interval", hours=24, id="cleanup-job")
    scheduler.start()
    return scheduler


