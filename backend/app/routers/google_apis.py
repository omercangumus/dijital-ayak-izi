"""
Google API'leri için router endpoint'leri
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from ..services.google_apis import (
    search_youtube_videos, 
    search_google_places, 
    analyze_image_with_vision, 
    get_geolocation_info
)

router = APIRouter(prefix="/api/google", tags=["Google APIs"])


class YouTubeSearchRequest(BaseModel):
    query: str
    max_results: int = 10


class PlacesSearchRequest(BaseModel):
    query: str
    location: Optional[str] = None
    radius: int = 50000


class ImageAnalysisRequest(BaseModel):
    image_url: str


class GeolocationRequest(BaseModel):
    address: str


@router.post("/youtube/search")
async def search_youtube(request: YouTubeSearchRequest):
    """
    YouTube'da video arama
    """
    try:
        results = search_youtube_videos(request.query, request.max_results)
        return {
            "success": True,
            "query": request.query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"YouTube arama hatası: {str(e)}")


@router.post("/places/search")
async def search_places(request: PlacesSearchRequest):
    """
    Google Places ile yer arama
    """
    try:
        results = search_google_places(request.query, request.location, request.radius)
        return {
            "success": True,
            "query": request.query,
            "location": request.location,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Places arama hatası: {str(e)}")


@router.post("/vision/analyze")
async def analyze_image(request: ImageAnalysisRequest):
    """
    Google Vision API ile görsel analiz
    """
    try:
        analysis = analyze_image_with_vision(request.image_url)
        return {
            "success": True,
            "image_url": request.image_url,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Görsel analiz hatası: {str(e)}")


@router.post("/geocoding/location")
async def get_location_info(request: GeolocationRequest):
    """
    Google Geocoding API ile adres bilgisi
    """
    try:
        location_info = get_geolocation_info(request.address)
        return {
            "success": True,
            "address": request.address,
            "location_info": location_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geocoding hatası: {str(e)}")


@router.get("/apis/status")
async def get_apis_status():
    """
    Google API'lerin durumunu kontrol et
    """
    from ..core.config import settings
    
    return {
        "google_api_key": bool(settings.google_api_key),
        "google_search_engine_id": bool(settings.google_search_engine_id),
        "google_maps_api_key": bool(settings.google_maps_api_key),
        "google_places_api_key": bool(settings.google_places_api_key),
        "google_youtube_api_key": bool(settings.google_youtube_api_key),
        "google_vision_api_key": bool(settings.google_vision_api_key)
    }
