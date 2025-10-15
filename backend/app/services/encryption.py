"""
API anahtarları için şifreleme servisi
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from ..core.config import settings


def generate_key_from_password(password: str, salt: bytes = None) -> bytes:
    """Şifre ve salt'tan anahtar üret"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


def encrypt_api_key(api_key: str, password: str) -> dict:
    """API anahtarını şifrele"""
    if not api_key:
        return {"encrypted": "", "salt": "", "error": "API key is empty"}
    
    try:
        key, salt = generate_key_from_password(password)
        fernet = Fernet(key)
        encrypted_key = fernet.encrypt(api_key.encode())
        
        return {
            "encrypted": base64.urlsafe_b64encode(encrypted_key).decode(),
            "salt": base64.urlsafe_b64encode(salt).decode(),
            "error": None
        }
    except Exception as e:
        return {"encrypted": "", "salt": "", "error": str(e)}


def decrypt_api_key(encrypted_data: str, salt: str, password: str) -> dict:
    """Şifrelenmiş API anahtarını çöz"""
    if not encrypted_data or not salt:
        return {"decrypted": "", "error": "Encrypted data or salt is empty"}
    
    try:
        # Salt'ı decode et
        salt_bytes = base64.urlsafe_b64decode(salt.encode())
        
        # Anahtarı üret
        key, _ = generate_key_from_password(password, salt_bytes)
        fernet = Fernet(key)
        
        # Şifrelenmiş veriyi decode et ve çöz
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_key = fernet.decrypt(encrypted_bytes)
        
        return {
            "decrypted": decrypted_key.decode(),
            "error": None
        }
    except Exception as e:
        return {"decrypted": "", "error": str(e)}


def get_encrypted_config() -> dict:
    """Şifrelenmiş konfigürasyon döndür"""
    password = settings.secret_key  # Şifre olarak secret key kullan
    
    config = {
        "google_api_key": encrypt_api_key(settings.google_api_key or "", password),
        "google_search_engine_id": encrypt_api_key(settings.google_search_engine_id or "", password),
        "google_maps_api_key": encrypt_api_key(settings.google_maps_api_key or "", password),
        "google_places_api_key": encrypt_api_key(settings.google_places_api_key or "", password),
        "google_youtube_api_key": encrypt_api_key(settings.google_youtube_api_key or "", password),
        "google_vision_api_key": encrypt_api_key(settings.google_vision_api_key or "", password),
        "scraperapi_key": encrypt_api_key(settings.scraperapi_key or "", password),
        "hibp_api_key": encrypt_api_key(settings.hibp_api_key or "", password)
    }
    
    return config


def get_decrypted_config() -> dict:
    """Şifrelenmiş konfigürasyondan orijinal değerleri al"""
    password = settings.secret_key
    
    # Şifrelenmiş değerler (gerçek uygulamada veritabanından gelecek)
    encrypted_config = get_encrypted_config()
    
    decrypted_config = {}
    for key, encrypted_data in encrypted_config.items():
        if encrypted_data.get("encrypted") and encrypted_data.get("salt"):
            result = decrypt_api_key(
                encrypted_data["encrypted"],
                encrypted_data["salt"],
                password
            )
            decrypted_config[key] = result.get("decrypted", "")
        else:
            decrypted_config[key] = ""
    
    return decrypted_config