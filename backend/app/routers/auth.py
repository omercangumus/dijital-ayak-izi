from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.user import User
from ..schemas.auth import RegisterRequest, RegisterResponse, VerifyRequest, VerifyResponse
from ..services.security import hash_email_for_storage, generate_email_verify_token, verify_email_token
from ..core.config import settings



router = APIRouter()


@router.get("/ping")
def ping():
    return {"message": "pong"}


@router.post("/register", response_model=RegisterResponse)
def register(req: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    if not req.consent:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="KVKK acik rizasi gerekli")

    email_hash = hash_email_for_storage(req.email)
    existing = db.query(User).filter(User.email_encrypted == email_hash).first()
    if existing:
        # Idempotent - tekrar kayit denemesinde dogrulama baglantisi uretilebilir
        token = generate_email_verify_token(req.email)
        return {"message": token}

    user = User(full_name=req.full_name, email_encrypted=email_hash, consent_accepted=True)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = generate_email_verify_token(req.email)
    # Not: E-posta gonderimi ileride eklenecek; simdilik token'i donuyoruz (egitim ortamı)
    return {"message": token}


@router.post("/verify", response_model=VerifyResponse)
def verify(req: VerifyRequest, db: Session = Depends(get_db)):
    email = verify_email_token(req.token, max_age_seconds=settings.email_verify_exp_hours * 3600)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Gecersiz veya suresi dolmus token")

    email_hash = hash_email_for_storage(email)
    user = db.query(User).filter(User.email_encrypted == email_hash).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanici bulunamadi")

    if not user.is_email_verified:
        user.is_email_verified = True
        db.add(user)
        db.commit()
    return {"message": "Email dogrulandi"}


