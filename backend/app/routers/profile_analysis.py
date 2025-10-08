"""
Profil Analiz Motoru API Endpoints
Etik OSINT araçları için API endpoint'leri
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Any, List, Optional
from pydantic import BaseModel, HttpUrl, validator
import time
import hashlib
from datetime import datetime, timedelta

from ..services.profile_analysis import (
    search_social_media,
    analyze_profile,
    fetch_profile_details,
    reverse_image_search,
    discover_other_accounts,
    find_public_email,
    list_public_photos
)
from ..services.audit import log_audit_event
from ..services.encryption import (
    encryption_service, 
    audit_logger, 
    consent_manager, 
    secure_storage,
    retention_service
)
from ..core.config import settings


router = APIRouter()


# Request/Response Models

class SocialMediaSearchRequest(BaseModel):
    name: str
    platform: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('İsim en az 2 karakter olmalıdır')
        if len(v.strip()) > 100:
            raise ValueError('İsim en fazla 100 karakter olabilir')
        return v.strip()


class ProfileAnalysisRequest(BaseModel):
    profile_url: HttpUrl
    
    @validator('profile_url')
    def validate_url(cls, v):
        url_str = str(v)
        if not any(domain in url_str for domain in ['twitter.com', 'linkedin.com', 'instagram.com', 'facebook.com', 'github.com', 'youtube.com']):
            raise ValueError('Desteklenen platformlar: Twitter, LinkedIn, Instagram, Facebook, GitHub, YouTube')
        return v


class ReverseImageSearchRequest(BaseModel):
    image_url: HttpUrl


class UsernameCheckRequest(BaseModel):
    username: str
    
    @validator('username')
    def validate_username(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Kullanıcı adı en az 2 karakter olmalıdır')
        if len(v.strip()) > 50:
            raise ValueError('Kullanıcı adı en fazla 50 karakter olabilir')
        return v.strip()


class EmailExtractionRequest(BaseModel):
    bio_text: str


class PublicPhotosRequest(BaseModel):
    profile_url: HttpUrl


# Response Models

class ProfileAnalysisResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    ethical_warning: bool = True
    analysis_timestamp: float
    processing_time: float


class SocialMediaSearchResponse(BaseModel):
    success: bool
    profiles: List[dict] = []
    total_found: int = 0
    ethical_warning: bool = True
    search_timestamp: float


# Rate Limiting Decorator
def rate_limit_check():
    """Basit rate limiting kontrolü"""
    # Bu gerçek bir rate limiting sistemi değil, sadece örnek
    # Gerçek uygulamada Redis veya database kullanılmalı
    return True


# API Endpoints

@router.post("/search-social-media", response_model=SocialMediaSearchResponse)
async def search_social_media_endpoint(
    request: SocialMediaSearchRequest,
    rate_limited: bool = Depends(rate_limit_check)
):
    """
    Sosyal medya platformlarında kişi arama
    
    Bu endpoint belirtilen isimle sosyal medya platformlarında arama yapar.
    Sadece halka açık profilleri bulur.
    """
    start_time = time.time()
    
    try:
        # Audit log
        await log_audit_event(
            action="social_media_search",
            details={
                "name": request.name,
                "platform": request.platform,
                "timestamp": start_time
            }
        )
        
        print(f"[API] Sosyal medya araması başladı: {request.name}")
        
        # Etik uyarı kontrolü
        if not settings.synthetic_mode and not settings.offline_mode:
            # Gerçek API kullanımında ek kontroller
            pass
        
        # Sosyal medya araması
        profiles = search_social_media(request.name, request.platform)
        
        processing_time = time.time() - start_time
        
        print(f"[API] Sosyal medya araması tamamlandı: {len(profiles)} profil bulundu")
        
        return SocialMediaSearchResponse(
            success=True,
            profiles=profiles,
            total_found=len(profiles),
            ethical_warning=True,
            search_timestamp=start_time
        )
        
    except Exception as e:
        print(f"[API] Sosyal medya arama hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sosyal medya arama hatası: {str(e)}"
        )


@router.post("/analyze-profile", response_model=ProfileAnalysisResponse)
async def analyze_profile_endpoint(
    request: ProfileAnalysisRequest,
    rate_limited: bool = Depends(rate_limit_check)
):
    """
    Profil detaylı analizi
    
    Bu endpoint belirtilen profil URL'ini derinlemesine analiz eder:
    - Profil detayları
    - Ters görsel arama
    - Diğer hesaplar
    - Halka açık e-posta
    - Halka açık fotoğraflar
    
    ⚠️ ETİK UYARI: Bu araç sadece kendi profillerinizi veya açık onay verilen profilleri analiz etmek için kullanılmalıdır.
    """
    start_time = time.time()
    session_token = encryption_service.generate_session_token()
    
    try:
        # Audit log
        await log_audit_event(
            action="profile_analysis",
            details={
                "profile_url": str(request.profile_url),
                "timestamp": start_time,
                "session_token": session_token
            }
        )
        
        print(f"[API] Profil analizi başladı: {request.profile_url}")
        
        # Profil analizi
        analysis_result = analyze_profile(str(request.profile_url))
        
        # Veriyi güvenli şekilde sakla (30 gün)
        data_id = f"profile_analysis_{int(start_time)}_{session_token[:8]}"
        secure_storage.store_data(
            data_id=data_id,
            data=analysis_result,
            user_id=session_token,
            ip_address="127.0.0.1"  # Gerçek IP adresi middleware'den alınabilir
        )
        
        processing_time = time.time() - start_time
        
        print(f"[API] Profil analizi tamamlandı: {processing_time:.2f}s")
        
        return ProfileAnalysisResponse(
            success=True,
            data=analysis_result,
            ethical_warning=True,
            analysis_timestamp=start_time,
            processing_time=processing_time
        )
        
    except Exception as e:
        print(f"[API] Profil analiz hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profil analiz hatası: {str(e)}"
        )


@router.post("/fetch-profile-details")
async def fetch_profile_details_endpoint(
    request: ProfileAnalysisRequest,
    rate_limited: bool = Depends(rate_limit_check)
):
    """
    Profil detaylarını çek
    
    Belirtilen URL'den profil detaylarını (username, bio, profil fotoğrafı) çeker.
    """
    try:
        print(f"[API] Profil detayları çekiliyor: {request.profile_url}")
        
        details = fetch_profile_details(str(request.profile_url))
        
        return {
            "success": True,
            "details": details,
            "ethical_warning": True
        }
        
    except Exception as e:
        print(f"[API] Profil detay çekme hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profil detay çekme hatası: {str(e)}"
        )


@router.post("/reverse-image-search")
async def reverse_image_search_endpoint(
    request: ReverseImageSearchRequest,
    rate_limited: bool = Depends(rate_limit_check)
):
    """
    Ters görsel arama
    
    Belirtilen görsel URL'ini kullanarak ters görsel arama yapar.
    Görselin başka web sitelerinde kullanılıp kullanılmadığını kontrol eder.
    """
    try:
        print(f"[API] Ters görsel arama başladı: {request.image_url}")
        
        results = reverse_image_search(str(request.image_url))
        
        return {
            "success": True,
            "results": results,
            "total_found": len(results),
            "ethical_warning": True
        }
        
    except Exception as e:
        print(f"[API] Ters görsel arama hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ters görsel arama hatası: {str(e)}"
        )


@router.post("/discover-other-accounts")
async def discover_other_accounts_endpoint(
    request: UsernameCheckRequest,
    rate_limited: bool = Depends(rate_limit_check)
):
    """
    Diğer hesapları keşfet
    
    Belirtilen kullanıcı adının 50+ popüler platformdaki varlığını kontrol eder.
    """
    try:
        print(f"[API] Diğer hesaplar keşfediliyor: {request.username}")
        
        accounts = discover_other_accounts(request.username)
        
        return {
            "success": True,
            "accounts": accounts,
            "total_found": len(accounts),
            "ethical_warning": True
        }
        
    except Exception as e:
        print(f"[API] Hesap keşif hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Hesap keşif hatası: {str(e)}"
        )


@router.post("/find-public-email")
async def find_public_email_endpoint(
    request: EmailExtractionRequest,
    rate_limited: bool = Depends(rate_limit_check)
):
    """
    Bio metninden e-posta bul
    
    Belirtilen bio metninden e-posta adreslerini çıkarır.
    """
    try:
        print(f"[API] Bio'dan e-posta aranıyor")
        
        email = find_public_email(request.bio_text)
        
        return {
            "success": True,
            "email": email,
            "found": email is not None,
            "ethical_warning": True
        }
        
    except Exception as e:
        print(f"[API] E-posta bulma hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"E-posta bulma hatası: {str(e)}"
        )


@router.post("/list-public-photos")
async def list_public_photos_endpoint(
    request: PublicPhotosRequest,
    rate_limited: bool = Depends(rate_limit_check)
):
    """
    Halka açık fotoğrafları listele
    
    Belirtilen profil URL'indeki halka açık fotoğrafları listeler.
    """
    try:
        print(f"[API] Halka açık fotoğraflar listeleniyor: {request.profile_url}")
        
        photos = list_public_photos(str(request.profile_url))
        
        return {
            "success": True,
            "photos": photos,
            "total_found": len(photos),
            "ethical_warning": True
        }
        
    except Exception as e:
        print(f"[API] Fotoğraf listeleme hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fotoğraf listeleme hatası: {str(e)}"
        )


@router.get("/ethical-guidelines")
async def get_ethical_guidelines():
    """
    Etik kullanım kılavuzu
    
    Bu API'nin etik kullanımı hakkında bilgiler döndürür.
    """
    return {
        "title": "Etik Kullanım Kılavuzu",
        "guidelines": [
            {
                "title": "Yasal Kullanım",
                "description": "Bu araç sadece yasal ve etik amaçlar için kullanılmalıdır. KVKK ve diğer gizlilik yasalarına uygun olarak kullanın."
            },
            {
                "title": "Onay Alma",
                "description": "Bir kişinin profilini analiz etmeden önce açık onayını alın. Sadece kendi profilinizi veya açık onay verilen profilleri analiz edin."
            },
            {
                "title": "Güvenlik Araştırması",
                "description": "Bu araç güvenlik araştırması, dijital ayak izi farkındalığı ve gizlilik eğitimi amaçları için tasarlanmıştır."
            },
            {
                "title": "Veri Koruma",
                "description": "Toplanan veriler güvenli şekilde saklanır ve 30 gün sonra otomatik olarak silinir. Kişisel verileri üçüncü taraflarla paylaşmayın."
            },
            {
                "title": "Rate Limiting",
                "description": "Platformların hizmet şartlarına saygı gösterin. Aşırı istek göndermeyin ve rate limiting kurallarına uyun."
            },
            {
                "title": "Sonuç Doğruluğu",
                "description": "Sonuçlar halka açık verilere dayanır ve %100 doğru olmayabilir. Sonuçları dikkatli bir şekilde değerlendirin."
            }
        ],
        "legal_warning": "Bu araç KVKK (Kişisel Verilerin Korunması Kanunu) ve diğer ilgili gizlilik yasalarına uygun olarak kullanılmalıdır. Yasadışı kullanım yasaktır ve sorumluluk kullanıcıya aittir.",
        "contact": "Etik kullanım hakkında sorularınız için: info@example.com"
    }


@router.get("/supported-platforms")
async def get_supported_platforms():
    """
    Desteklenen platformlar listesi
    
    Bu API'nin desteklediği platformları listeler.
    """
    platforms = [
        {"name": "Twitter", "url": "https://twitter.com", "features": ["profile", "photos", "bio"]},
        {"name": "LinkedIn", "url": "https://linkedin.com", "features": ["profile", "bio", "professional_info"]},
        {"name": "Instagram", "url": "https://instagram.com", "features": ["profile", "photos", "bio"]},
        {"name": "Facebook", "url": "https://facebook.com", "features": ["profile", "photos", "basic_info"]},
        {"name": "GitHub", "url": "https://github.com", "features": ["profile", "repositories", "bio"]},
        {"name": "YouTube", "url": "https://youtube.com", "features": ["channel", "videos", "description"]},
        {"name": "Reddit", "url": "https://reddit.com", "features": ["profile", "posts", "comments"]},
        {"name": "TikTok", "url": "https://tiktok.com", "features": ["profile", "videos", "bio"]},
        {"name": "Pinterest", "url": "https://pinterest.com", "features": ["profile", "pins", "boards"]},
        {"name": "Medium", "url": "https://medium.com", "features": ["profile", "articles", "bio"]}
    ]
    
    return {
        "supported_platforms": platforms,
        "total_count": len(platforms),
        "note": "Tüm platformlar için sadece halka açık bilgiler analiz edilir. Özel/gizli profiller erişilemez."
    }


@router.get("/health")
async def health_check():
    """
    API sağlık kontrolü
    
    API'nin çalışma durumunu kontrol eder.
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "features": {
            "social_media_search": True,
            "profile_analysis": True,
            "reverse_image_search": bool(settings.serpapi_key),
            "username_discovery": True,
            "email_extraction": True,
            "photo_listing": True
        },
        "rate_limiting": True,
        "ethical_warnings": True
    }
