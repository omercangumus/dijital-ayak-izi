"""
API şifreleme router'ı
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from ..services.encryption import get_encrypted_config, get_decrypted_config, encrypt_api_key, decrypt_api_key

router = APIRouter(prefix="/api/encryption", tags=["Encryption"])


class EncryptRequest(BaseModel):
    api_key: str
    password: str


class DecryptRequest(BaseModel):
    encrypted_data: str
    salt: str
    password: str


@router.post("/encrypt")
async def encrypt_key(request: EncryptRequest):
    """
    API anahtarını şifrele
    """
    try:
        result = encrypt_api_key(request.api_key, request.password)
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "encrypted": result["encrypted"],
            "salt": result["salt"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Şifreleme hatası: {str(e)}")


@router.post("/decrypt")
async def decrypt_key(request: DecryptRequest):
    """
    Şifrelenmiş API anahtarını çöz
    """
    try:
        result = decrypt_api_key(request.encrypted_data, request.salt, request.password)
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "decrypted": result["decrypted"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Çözme hatası: {str(e)}")


@router.get("/config/encrypted")
async def get_encrypted_config_endpoint():
    """
    Şifrelenmiş konfigürasyonu getir
    """
    try:
        config = get_encrypted_config()
        return {
            "success": True,
            "encrypted_config": config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Konfigürasyon hatası: {str(e)}")


@router.get("/config/decrypted")
async def get_decrypted_config_endpoint():
    """
    Çözülmüş konfigürasyonu getir
    """
    try:
        config = get_decrypted_config()
        return {
            "success": True,
            "decrypted_config": config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Konfigürasyon hatası: {str(e)}")


@router.get("/status")
async def encryption_status():
    """
    Şifreleme durumunu kontrol et
    """
    try:
        encrypted_config = get_encrypted_config()
        
        status = {}
        for key, data in encrypted_config.items():
            status[key] = {
                "encrypted": bool(data.get("encrypted")),
                "has_salt": bool(data.get("salt")),
                "error": data.get("error")
            }
        
        return {
            "success": True,
            "encryption_status": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Durum kontrolü hatası: {str(e)}")
