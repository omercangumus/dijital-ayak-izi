#!/usr/bin/env python3
"""
Basit FastAPI sunucusu - Ana dizinden çalıştırılabilir
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Backend modüllerini import et
from backend.app.routers import auth, selfscan, image
from backend.app.core.config import settings

app = FastAPI(
    title="Siber Güvenlik Projesi",
    description="Platform bazlı arama ve güvenlik analizi",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(selfscan.router, prefix="/api", tags=["selfscan"])
app.include_router(image.router, prefix="/api", tags=["image"])

# Gelişmiş arama endpoint'leri
@app.post("/api/verify-platform-profile")
async def verify_platform_profile(request: dict):
    """Platform profilini doğrula"""
    platform = request.get("platform")
    profile_url = request.get("profile_url")
    
    # Mock doğrulama
    verified_profile = {
        "platform": platform,
        "profile_url": profile_url,
        "verified": True,
        "user_id": "demo_user_123",
        "username": "demo_user",
        "display_name": "Demo User",
        "profile_picture": "https://via.placeholder.com/150",
        "verification_timestamp": "2024-01-01T00:00:00Z",
        "public_info": {
            "followers_count": 1000,
            "posts_count": 150,
            "verified_account": True
        }
    }
    
    return {
        "status": "success",
        "verified_profile": verified_profile,
        "verification_method": "demo_verification"
    }

@app.post("/api/analyze-image-advanced")
async def analyze_image_advanced(request: dict):
    """Gelişmiş resim analizi"""
    image_url = request.get("image_url")
    analysis_type = request.get("analysis_type", "face_recognition")
    
    # Mock analiz sonuçları
    analysis_results = {
        "image_url": image_url,
        "analysis_type": analysis_type,
        "results": {
            "faces_detected": 1,
            "face_confidence": 0.95,
            "estimated_age": "25-30",
            "emotions": ["happy", "confident"],
            "objects_detected": ["person", "background"],
            "text_extracted": ["Demo Text"],
            "similar_images": [
                "https://example.com/similar1.jpg",
                "https://example.com/similar2.jpg"
            ],
            "reverse_image_search": {
                "total_results": 15,
                "sources": [
                    {"platform": "facebook", "url": "https://facebook.com/profile1"},
                    {"platform": "linkedin", "url": "https://linkedin.com/profile1"},
                    {"platform": "twitter", "url": "https://twitter.com/profile1"}
                ]
            }
        }
    }
    
    return analysis_results

@app.post("/api/advanced-profile-search")
async def advanced_profile_search(request: dict):
    """Doğrulanmış profil üzerinden gelişmiş arama"""
    verified_profile = request.get("verified_profile")
    search_depth = request.get("search_depth", "deep")
    include_image_analysis = request.get("include_image_analysis", True)
    
    # Mock arama sonuçları
    search_results = [
        {
            "query": f'"{verified_profile["display_name"]}"',
            "platform": verified_profile["platform"],
            "results": [
                {
                    "title": f"{verified_profile['display_name']} - {verified_profile['platform']} Profili",
                    "url": verified_profile["profile_url"],
                    "snippet": f"{verified_profile['display_name']} kullanıcısının {verified_profile['platform']} profili",
                    "confidence": 0.95,
                    "source": verified_profile["platform"]
                }
            ]
        }
    ]
    
    # Resim analizi
    image_analysis = None
    if include_image_analysis and verified_profile.get("profile_picture"):
        image_analysis = {
            "image_url": verified_profile["profile_picture"],
            "analysis_type": "face_recognition",
            "results": {
                "faces_detected": 1,
                "face_confidence": 0.95,
                "reverse_image_search": {
                    "total_results": 15,
                    "sources": [
                        {"platform": "facebook", "url": "https://facebook.com/profile1"},
                        {"platform": "linkedin", "url": "https://linkedin.com/profile1"}
                    ]
                }
            }
        }
    
    return {
        "status": "success",
        "verified_profile": verified_profile,
        "search_results": search_results,
        "image_analysis": image_analysis,
        "search_metadata": {
            "search_depth": search_depth,
            "analysis_timestamp": "2024-01-01T00:00:00Z"
        }
    }

# Static dosyalar - sadece frontend dosyaları için
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return {"message": "Siber Güvenlik Projesi API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Sunucu çalışıyor"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "message": "API çalışıyor"}

@app.get("/app")
async def frontend():
    """Frontend uygulaması"""
    from fastapi.responses import FileResponse
    return FileResponse("index.html")

if __name__ == "__main__":
    print("🚀 Sunucu başlatılıyor...")
    print("📱 Frontend: http://localhost:8000")
    print("🔧 API: http://localhost:8000/api")
    print("📖 Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
