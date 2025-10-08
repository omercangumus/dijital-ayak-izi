#!/usr/bin/env python3
"""
Ethical OSINT Server
- FastAPI tabanlı backend
- KVKK ve etik kurallara uygun
- Güvenli veri işleme
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
import uvicorn
import os
from datetime import datetime, timedelta
import hashlib
import json
import asyncio

# Local imports
from ethical_osint import osint_engine, ProfileInfo, SearchResult

app = FastAPI(
    title="Ethical OSINT Profile Analysis Engine",
    description="KVKK ve etik kurallara uygun açık kaynak istihbarat aracı",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class SearchRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Aranacak kişinin adı")
    platform: str = Field(..., min_length=2, max_length=50, description="Arama platformu")
    
    @validator('name')
    def validate_name(cls, v):
        # Sadece harf, sayı ve boşluk
        if not re.match(r'^[a-zA-Z0-9\s]+$', v):
            raise ValueError('İsim sadece harf, sayı ve boşluk içerebilir')
        return v.strip()

class AnalysisRequest(BaseModel):
    profile_url: str = Field(..., description="Analiz edilecek profil URL'si")
    
    @validator('profile_url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Geçerli bir URL giriniz')
        return v

class EthicalConsentRequest(BaseModel):
    consent_given: bool = Field(..., description="Etik onay verildi mi?")
    purpose: str = Field(..., description="Kullanım amacı")
    data_retention_days: int = Field(default=1, ge=1, le=30, description="Veri saklama süresi (gün)")

# Session storage (memory-based, production'da Redis kullanılmalı)
session_storage = {}
SESSION_TIMEOUT = timedelta(hours=1)

def get_session_id(request: Request) -> str:
    """Session ID oluştur"""
    client_ip = request.client.host
    user_agent = request.headers.get('user-agent', '')
    session_key = f"{client_ip}_{user_agent}_{datetime.now().strftime('%Y%m%d%H')}"
    return hashlib.md5(session_key.encode()).hexdigest()

def check_ethical_consent(session_id: str) -> bool:
    """Etik onay kontrolü"""
    if session_id in session_storage:
        session_data = session_storage[session_id]
        if datetime.now() - session_data['consent_time'] < SESSION_TIMEOUT:
            return session_data.get('consent_given', False)
    return False

# API Endpoints
@app.post("/api/ethical-consent")
async def give_ethical_consent(
    consent: EthicalConsentRequest,
    request: Request
):
    """Etik onay verme endpoint'i"""
    session_id = get_session_id(request)
    
    if not consent.consent_given:
        raise HTTPException(status_code=400, detail="Etik onay verilmeden devam edilemez")
    
    # Onay verilerini sakla
    session_storage[session_id] = {
        'consent_given': True,
        'purpose': consent.purpose,
        'data_retention_days': consent.data_retention_days,
        'consent_time': datetime.now()
    }
    
    return {
        "status": "success",
        "message": "Etik onay kaydedildi",
        "session_id": session_id,
        "retention_days": consent.data_retention_days
    }

@app.post("/api/search-profiles")
async def search_profiles(
    search_req: SearchRequest,
    request: Request
):
    """Profil arama endpoint'i"""
    session_id = get_session_id(request)
    
    if not check_ethical_consent(session_id):
        raise HTTPException(
            status_code=403, 
            detail="Etik onay verilmeden arama yapılamaz. Önce /api/ethical-consent endpoint'ini kullanın."
        )
    
    try:
        # Rate limiting kontrolü
        if session_id in session_storage:
            last_search = session_storage[session_id].get('last_search_time')
            if last_search and datetime.now() - last_search < timedelta(minutes=1):
                raise HTTPException(
                    status_code=429, 
                    detail="Çok hızlı arama yapıyorsunuz. Lütfen 1 dakika bekleyin."
                )
        
        # Arama işlemi
        search_result = osint_engine.search_social_media(
            search_req.name, 
            search_req.platform
        )
        
        # Session güncelleme
        if session_id in session_storage:
            session_storage[session_id]['last_search_time'] = datetime.now()
            session_storage[session_id]['last_search'] = {
                'name': search_req.name,
                'platform': search_req.platform,
                'results_count': len(search_result.profiles),
                'timestamp': datetime.now().isoformat()
            }
        
        return {
            "status": "success",
            "data": {
                "profiles": [
                    {
                        "username": p.username,
                        "display_name": p.display_name,
                        "bio": p.bio,
                        "profile_picture": p.profile_picture,
                        "platform": p.platform,
                        "url": p.url,
                        "followers_count": p.followers_count,
                        "verified": p.verified
                    } for p in search_result.profiles
                ],
                "total_found": search_result.total_found,
                "search_time": search_result.search_time,
                "search_timestamp": datetime.now().isoformat()
            },
            "warnings": [
                "Sonuçlar sadece açık kaynak verilerden alınmıştır",
                "Veriler %100 doğru olmayabilir",
                "Platform kullanım şartlarına uygun hareket edilmiştir"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Arama hatası: {str(e)}")

@app.post("/api/analyze-profile")
async def analyze_profile(
    analysis_req: AnalysisRequest,
    request: Request
):
    """Profil analiz endpoint'i"""
    session_id = get_session_id(request)
    
    if not check_ethical_consent(session_id):
        raise HTTPException(
            status_code=403, 
            detail="Etik onay verilmeden analiz yapılamaz"
        )
    
    try:
        # Analiz işlemi
        analysis_result = osint_engine.analyze_profile(analysis_req.profile_url)
        
        # Session güncelleme
        if session_id in session_storage:
            session_storage[session_id]['last_analysis'] = {
                'url': analysis_req.profile_url,
                'timestamp': datetime.now().isoformat(),
                'results_count': len(analysis_result.get('other_accounts', []))
            }
        
        return {
            "status": "success",
            "data": analysis_result,
            "ethical_notice": {
                "data_retention": f"{session_storage.get(session_id, {}).get('data_retention_days', 1)} gün",
                "purpose": session_storage.get(session_id, {}).get('purpose', 'Bilinmiyor'),
                "consent_timestamp": session_storage.get(session_id, {}).get('consent_time', '').isoformat() if session_storage.get(session_id, {}).get('consent_time') else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analiz hatası: {str(e)}")

@app.get("/api/search-status")
async def search_status(request: Request):
    """Arama durumu kontrolü"""
    session_id = get_session_id(request)
    
    if session_id not in session_storage:
        return {
            "status": "no_session",
            "consent_given": False,
            "message": "Etik onay verilmemiş"
        }
    
    session_data = session_storage[session_id]
    consent_valid = datetime.now() - session_data['consent_time'] < SESSION_TIMEOUT
    
    return {
        "status": "active" if consent_valid else "expired",
        "consent_given": consent_valid,
        "session_id": session_id,
        "consent_time": session_data['consent_time'].isoformat(),
        "retention_days": session_data.get('data_retention_days', 1),
        "purpose": session_data.get('purpose', 'Bilinmiyor'),
        "last_search": session_data.get('last_search'),
        "last_analysis": session_data.get('last_analysis')
    }

@app.delete("/api/clear-session")
async def clear_session(request: Request):
    """Session temizleme (KVKK uyumu için)"""
    session_id = get_session_id(request)
    
    if session_id in session_storage:
        del session_storage[session_id]
        return {
            "status": "success",
            "message": "Session verileri temizlendi"
        }
    
    return {
        "status": "success", 
        "message": "Temizlenecek session bulunamadı"
    }

@app.get("/api/health")
async def health_check():
    """Sistem durumu kontrolü"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(session_storage),
        "ethical_compliance": "KVKK ve etik kurallara uygun",
        "data_retention_policy": "Otomatik temizleme aktif"
    }

# Static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Frontend serving
@app.get("/", response_class=HTMLResponse)
async def frontend():
    """Ana sayfa"""
    return FileResponse("ethical_frontend.html")

@app.get("/app", response_class=HTMLResponse)
async def app_page():
    """Uygulama sayfası"""
    return FileResponse("ethical_frontend.html")

# Cleanup task (KVKK uyumu için otomatik veri temizleme)
async def cleanup_expired_sessions():
    """Süresi dolmuş session'ları temizle"""
    while True:
        try:
            current_time = datetime.now()
            expired_sessions = []
            
            for session_id, session_data in session_storage.items():
                if current_time - session_data['consent_time'] > SESSION_TIMEOUT:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del session_storage[session_id]
            
            if expired_sessions:
                print(f"🧹 {len(expired_sessions)} süresi dolmuş session temizlendi")
            
            await asyncio.sleep(300)  # 5 dakikada bir kontrol et
            
        except Exception as e:
            print(f"Session temizleme hatası: {e}")
            await asyncio.sleep(60)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Uygulama başlatma"""
    print("🚀 Ethical OSINT Engine başlatılıyor...")
    print("📋 KVKK ve etik kurallara uygun")
    print("🔒 Güvenli veri işleme aktif")
    
    # Cleanup task'i başlat
    asyncio.create_task(cleanup_expired_sessions())

if __name__ == "__main__":
    import re
    from fastapi.responses import FileResponse
    
    print("""
    ⚖️  ETHICAL OSINT PROFILE ANALYSIS ENGINE ⚖️
    
    🔒 KVKK ve Etik Kurallar:
    - Sadece açık kaynak veriler kullanılır
    - Kullanıcı onayı zorunludur
    - Otomatik veri temizleme aktif
    - Platform kullanım şartlarına uyum
    
    ⚠️  UYARI: Bu araç sadece yasal ve etik amaçlarla kullanılmalıdır!
    
    🚀 Sunucu başlatılıyor...
    """)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
