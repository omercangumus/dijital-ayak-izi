"""
Veri Şifreleme Servisi
KVKK uyumlu veri güvenliği için şifreleme araçları
"""

import os
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
import json


class DataEncryption:
    """Veri şifreleme ve güvenlik sınıfı"""
    
    def __init__(self):
        # Anahtar üretimi için salt
        self.salt = self._get_or_create_salt()
        # Şifreleme anahtarı
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_or_create_salt(self) -> bytes:
        """Salt değeri al veya oluştur"""
        salt_file = "backend/data/salt.key"
        os.makedirs(os.path.dirname(salt_file), exist_ok=True)
        
        if os.path.exists(salt_file):
            with open(salt_file, 'rb') as f:
                return f.read()
        else:
            # Yeni salt oluştur
            salt = os.urandom(32)
            with open(salt_file, 'wb') as f:
                f.write(salt)
            return salt
    
    def _get_or_create_key(self) -> bytes:
        """Şifreleme anahtarı al veya oluştur"""
        key_file = "backend/data/encryption.key"
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Yeni anahtar oluştur
            password = os.environ.get('ENCRYPTION_PASSWORD', 'default-password-change-in-production')
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_data(self, data: Dict[str, Any]) -> str:
        """Veriyi şifrele"""
        try:
            # Veriyi JSON string'e çevir
            json_data = json.dumps(data, ensure_ascii=False)
            
            # Şifrele
            encrypted_data = self.cipher.encrypt(json_data.encode())
            
            # Base64 ile encode et
            encoded_data = base64.b64encode(encrypted_data).decode()
            
            return encoded_data
        except Exception as e:
            print(f"[X] Veri şifreleme hatası: {str(e)}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Şifrelenmiş veriyi çöz"""
        try:
            # Base64 decode
            decoded_data = base64.b64decode(encrypted_data.encode())
            
            # Şifreyi çöz
            decrypted_data = self.cipher.decrypt(decoded_data)
            
            # JSON parse et
            json_data = json.loads(decrypted_data.decode())
            
            return json_data
        except Exception as e:
            print(f"[X] Veri çözme hatası: {str(e)}")
            raise
    
    def hash_sensitive_data(self, data: str) -> str:
        """Hassas verileri hash'le (geri çözülemez)"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def generate_session_token(self) -> str:
        """Güvenli oturum token'ı oluştur"""
        return secrets.token_urlsafe(32)
    
    def sanitize_personal_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Kişisel verileri temizle ve hassas bilgileri maskele"""
        sanitized = data.copy()
        
        # Hassas alanları maskele
        sensitive_fields = ['email', 'phone', 'address', 'full_name', 'username']
        
        for field in sensitive_fields:
            if field in sanitized and sanitized[field]:
                if isinstance(sanitized[field], str):
                    # İlk ve son karakterleri göster, ortasını maskele
                    value = sanitized[field]
                    if len(value) > 4:
                        sanitized[field] = value[0] + '*' * (len(value) - 2) + value[-1]
                    else:
                        sanitized[field] = '*' * len(value)
        
        return sanitized


class DataRetention:
    """Veri saklama politikası yöneticisi"""
    
    def __init__(self):
        self.retention_days = 30  # 30 gün saklama süresi
    
    def is_data_expired(self, creation_timestamp: float) -> bool:
        """Verinin süresi dolmuş mu kontrol et"""
        creation_date = datetime.fromtimestamp(creation_timestamp)
        expiration_date = creation_date + timedelta(days=self.retention_days)
        return datetime.now() > expiration_date
    
    def get_expiration_date(self, creation_timestamp: float) -> datetime:
        """Verinin sona erme tarihini hesapla"""
        creation_date = datetime.fromtimestamp(creation_timestamp)
        return creation_date + timedelta(days=self.retention_days)
    
    def should_auto_delete(self, data: Dict[str, Any]) -> bool:
        """Verinin otomatik silinmesi gerekiyor mu"""
        if 'creation_timestamp' in data:
            return self.is_data_expired(data['creation_timestamp'])
        return False


class AuditLogger:
    """KVKK uyumlu audit log sistemi"""
    
    def __init__(self):
        self.log_file = "backend/data/audit.log"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log_access(self, user_id: str, action: str, resource: str, ip_address: str):
        """Erişim logu kaydet"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "ip_address": ip_address,
            "type": "access"
        }
        self._write_log(log_entry)
    
    def log_data_access(self, user_id: str, data_type: str, data_id: str, ip_address: str):
        """Veri erişim logu kaydet"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "data_type": data_type,
            "data_id": data_id,
            "ip_address": ip_address,
            "type": "data_access"
        }
        self._write_log(log_entry)
    
    def log_data_deletion(self, user_id: str, data_type: str, data_id: str, reason: str):
        """Veri silme logu kaydet"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "data_type": data_type,
            "data_id": data_id,
            "reason": reason,
            "type": "data_deletion"
        }
        self._write_log(log_entry)
    
    def _write_log(self, log_entry: Dict[str, Any]):
        """Log dosyasına yaz"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"[X] Log yazma hatası: {str(e)}")


class ConsentManager:
    """KVKK onay yönetimi"""
    
    def __init__(self):
        self.consent_file = "backend/data/consents.json"
        self.encryption = DataEncryption()
        self.retention = DataRetention()
    
    def record_consent(self, user_id: str, consent_type: str, granted: bool, 
                      ip_address: str, user_agent: str) -> str:
        """Onay kaydı oluştur"""
        consent_id = self.encryption.generate_session_token()
        
        consent_data = {
            "consent_id": consent_id,
            "user_id": user_id,
            "consent_type": consent_type,
            "granted": granted,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "timestamp": datetime.now().timestamp(),
            "creation_timestamp": datetime.now().timestamp()
        }
        
        # Şifrele ve kaydet
        encrypted_data = self.encryption.encrypt_data(consent_data)
        
        # Dosyaya kaydet
        self._save_consent(consent_id, encrypted_data)
        
        return consent_id
    
    def get_consent(self, consent_id: str) -> Optional[Dict[str, Any]]:
        """Onay kaydını al"""
        try:
            encrypted_data = self._load_consent(consent_id)
            if not encrypted_data:
                return None
            
            consent_data = self.encryption.decrypt_data(encrypted_data)
            
            # Süresi dolmuş mu kontrol et
            if self.retention.should_auto_delete(consent_data):
                self.revoke_consent(consent_id, "expired")
                return None
            
            return consent_data
        except Exception as e:
            print(f"[X] Onay kaydı okuma hatası: {str(e)}")
            return None
    
    def revoke_consent(self, consent_id: str, reason: str = "user_request"):
        """Onayı iptal et"""
        try:
            self._delete_consent(consent_id)
            print(f"[OK] Onay iptal edildi: {consent_id}, Sebep: {reason}")
        except Exception as e:
            print(f"[X] Onay iptal hatası: {str(e)}")
    
    def _save_consent(self, consent_id: str, encrypted_data: str):
        """Onay kaydını dosyaya kaydet"""
        os.makedirs(os.path.dirname(self.consent_file), exist_ok=True)
        
        consents = {}
        if os.path.exists(self.consent_file):
            with open(self.consent_file, 'r', encoding='utf-8') as f:
                consents = json.load(f)
        
        consents[consent_id] = encrypted_data
        
        with open(self.consent_file, 'w', encoding='utf-8') as f:
            json.dump(consents, f, ensure_ascii=False, indent=2)
    
    def _load_consent(self, consent_id: str) -> Optional[str]:
        """Onay kaydını dosyadan yükle"""
        if not os.path.exists(self.consent_file):
            return None
        
        with open(self.consent_file, 'r', encoding='utf-8') as f:
            consents = json.load(f)
        
        return consents.get(consent_id)
    
    def _delete_consent(self, consent_id: str):
        """Onay kaydını sil"""
        if not os.path.exists(self.consent_file):
            return
        
        with open(self.consent_file, 'r', encoding='utf-8') as f:
            consents = json.load(f)
        
        if consent_id in consents:
            del consents[consent_id]
            
            with open(self.consent_file, 'w', encoding='utf-8') as f:
                json.dump(consents, f, ensure_ascii=False, indent=2)


class SecureDataStorage:
    """Güvenli veri saklama sistemi"""
    
    def __init__(self):
        self.encryption = DataEncryption()
        self.retention = DataRetention()
        self.audit = AuditLogger()
        self.storage_file = "backend/data/secure_storage.json"
    
    def store_data(self, data_id: str, data: Dict[str, Any], user_id: str, ip_address: str) -> bool:
        """Veriyi güvenli şekilde sakla"""
        try:
            # Veriye metadata ekle
            data_with_metadata = {
                "data_id": data_id,
                "user_id": user_id,
                "creation_timestamp": datetime.now().timestamp(),
                "ip_address": ip_address,
                "data": data
            }
            
            # Şifrele
            encrypted_data = self.encryption.encrypt_data(data_with_metadata)
            
            # Dosyaya kaydet
            self._save_to_storage(data_id, encrypted_data)
            
            # Audit log
            self.audit.log_data_access(user_id, "store", data_id, ip_address)
            
            print(f"[OK] Veri güvenli şekilde saklandı: {data_id}")
            return True
            
        except Exception as e:
            print(f"[X] Veri saklama hatası: {str(e)}")
            return False
    
    def retrieve_data(self, data_id: str, user_id: str, ip_address: str) -> Optional[Dict[str, Any]]:
        """Veriyi güvenli şekilde al"""
        try:
            encrypted_data = self._load_from_storage(data_id)
            if not encrypted_data:
                return None
            
            data_with_metadata = self.encryption.decrypt_data(encrypted_data)
            
            # Süresi dolmuş mu kontrol et
            if self.retention.should_auto_delete(data_with_metadata):
                self.delete_data(data_id, user_id, "expired")
                return None
            
            # Audit log
            self.audit.log_data_access(user_id, "retrieve", data_id, ip_address)
            
            return data_with_metadata.get("data")
            
        except Exception as e:
            print(f"[X] Veri alma hatası: {str(e)}")
            return None
    
    def delete_data(self, data_id: str, user_id: str, reason: str = "user_request"):
        """Veriyi sil"""
        try:
            self._delete_from_storage(data_id)
            
            # Audit log
            self.audit.log_data_deletion(user_id, "delete", data_id, reason)
            
            print(f"[OK] Veri silindi: {data_id}, Sebep: {reason}")
            
        except Exception as e:
            print(f"[X] Veri silme hatası: {str(e)}")
    
    def cleanup_expired_data(self):
        """Süresi dolmuş verileri temizle"""
        try:
            if not os.path.exists(self.storage_file):
                return
            
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            expired_keys = []
            for data_id, encrypted_data in storage.items():
                try:
                    data_with_metadata = self.encryption.decrypt_data(encrypted_data)
                    if self.retention.should_auto_delete(data_with_metadata):
                        expired_keys.append(data_id)
                except:
                    # Şifreli veri bozuksa sil
                    expired_keys.append(data_id)
            
            # Süresi dolmuş verileri sil
            for key in expired_keys:
                del storage[key]
                print(f"[OK] Süresi dolmuş veri silindi: {key}")
            
            # Güncellenmiş storage'ı kaydet
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(storage, f, ensure_ascii=False, indent=2)
            
            print(f"[OK] Toplam {len(expired_keys)} süresi dolmuş veri temizlendi")
            
        except Exception as e:
            print(f"[X] Veri temizleme hatası: {str(e)}")
    
    def _save_to_storage(self, data_id: str, encrypted_data: str):
        """Veriyi storage dosyasına kaydet"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        
        storage = {}
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                storage = json.load(f)
        
        storage[data_id] = encrypted_data
        
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)
    
    def _load_from_storage(self, data_id: str) -> Optional[str]:
        """Veriyi storage dosyasından yükle"""
        if not os.path.exists(self.storage_file):
            return None
        
        with open(self.storage_file, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        return storage.get(data_id)
    
    def _delete_from_storage(self, data_id: str):
        """Veriyi storage dosyasından sil"""
        if not os.path.exists(self.storage_file):
            return
        
        with open(self.storage_file, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        if data_id in storage:
            del storage[data_id]
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(storage, f, ensure_ascii=False, indent=2)


# Global instances
encryption_service = DataEncryption()
retention_service = DataRetention()
audit_logger = AuditLogger()
consent_manager = ConsentManager()
secure_storage = SecureDataStorage()


def cleanup_expired_data():
    """Süresi dolmuş verileri temizle - scheduled task için"""
    secure_storage.cleanup_expired_data()
    print("[OK] Otomatik veri temizleme tamamlandı")
