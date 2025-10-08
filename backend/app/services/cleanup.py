from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..models.audit import AuditLog
from .encryption import cleanup_expired_data


def cleanup_old_data(days: int = 30):
    """Eski audit loglarını temizle"""
    db = SessionLocal()
    try:
        threshold = datetime.utcnow() - timedelta(days=days)
        deleted_count = db.query(AuditLog).filter(AuditLog.created_at < threshold).delete()
        db.commit()
        print(f"[OK] {deleted_count} eski audit log temizlendi")
    except Exception as e:
        print(f"[X] Audit log temizleme hatası: {str(e)}")
        db.rollback()
    finally:
        db.close()


def cleanup_encrypted_data():
    """Şifrelenmiş verileri temizle"""
    try:
        cleanup_expired_data()
    except Exception as e:
        print(f"[X] Şifrelenmiş veri temizleme hatası: {str(e)}")


def start_scheduler():
    """Zamanlanmış görevleri başlat"""
    scheduler = BackgroundScheduler()
    
    # Audit log temizleme (günde bir)
    scheduler.add_job(
        cleanup_old_data, 
        "interval", 
        hours=24, 
        id="audit-cleanup-job",
        next_run_time=datetime.utcnow()
    )
    
    # Şifrelenmiş veri temizleme (günde bir)
    scheduler.add_job(
        cleanup_encrypted_data,
        "interval",
        hours=24,
        id="encrypted-data-cleanup-job",
        next_run_time=datetime.utcnow()
    )
    
    scheduler.start()
    print("[OK] Zamanlanmış temizleme görevleri başlatıldı")
    return scheduler


