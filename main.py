#!/usr/bin/env python3
"""
Sosyal Medya Profil Analiz API Server

Bu FastAPI uygulaması, sosyal medya profillerini analiz eden bir web API sunar:
1. Scraper API ile profil verilerini çeker
2. Google Custom Search API ile ters görsel arama yapar
3. Sonuçları JSON formatında döndürür

API Endpoint: POST /analyze
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from urllib.parse import urlparse, urljoin
import time
import logging
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables yükle
load_dotenv()

# FastAPI app instance
app = FastAPI(
    title="Sosyal Medya Profil Analiz API",
    description="Sosyal medya profillerini analiz eden API servisi",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da belirli domain'leri belirtin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class AnalyzeRequest(BaseModel):
    """Analiz isteği modeli"""
    profile_url: HttpUrl
    
    class Config:
        schema_extra = {
            "example": {
                "profile_url": "https://www.instagram.com/nasa/"
            }
        }

class AnalyzeResponse(BaseModel):
    """Analiz yanıt modeli"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: int
    processing_time: float

# Profile Analyzer Class
class ProfileAnalyzer:
    """Sosyal medya profil analiz sınıfı"""
    
    def __init__(self):
        """API anahtarlarını .env dosyasından yükle"""
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.scraper_api_key = os.getenv('SCRAPER_API_KEY')
        
        # API anahtarlarının varlığını kontrol et
        self._validate_api_keys()
        
        # Google Custom Search servisini başlat
        self.google_service = build(
            "customsearch", 
            "v1", 
            developerKey=self.google_api_key
        )
        
        logger.info("ProfileAnalyzer başarıyla başlatıldı")
    
    def _validate_api_keys(self):
        """API anahtarlarının varlığını kontrol et"""
        missing_keys = []
        
        if not self.google_api_key:
            missing_keys.append('GOOGLE_API_KEY')
        if not self.google_search_engine_id:
            missing_keys.append('GOOGLE_SEARCH_ENGINE_ID')
        if not self.scraper_api_key:
            missing_keys.append('SCRAPER_API_KEY')
        
        if missing_keys:
            raise ValueError(f"Eksik API anahtarları: {', '.join(missing_keys)}")
        
        logger.info("Tüm API anahtarları doğrulandı")
    
    def scrape_profile(self, profile_url: str) -> Dict[str, Any]:
        """
        Scraper API kullanarak profil verilerini çek
        
        Args:
            profile_url (str): Analiz edilecek profil URL'i
            
        Returns:
            dict: Profil verileri
        """
        try:
            logger.info(f"Profil scraping başlatıldı: {profile_url}")
            
            # Scraper API endpoint
            scraper_url = "http://api.scraperapi.com"
            
            params = {
                'api_key': self.scraper_api_key,
                'url': profile_url,
                'render': 'true',  # JavaScript render
                'country_code': 'us'
            }
            
            response = requests.get(scraper_url, params=params, timeout=30)
            response.raise_for_status()
            
            # HTML'i parse et
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Profil verilerini çıkar
            profile_data = self._extract_profile_data(soup, profile_url)
            
            logger.info("Profil scraping başarıyla tamamlandı")
            return profile_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Scraping hatası: {str(e)}")
            raise Exception(f"Profil scraping başarısız: {str(e)}")
        except Exception as e:
            logger.error(f"Beklenmeyen hata: {str(e)}")
            raise Exception(f"Profil analizi hatası: {str(e)}")
    
    def _extract_profile_data(self, soup: BeautifulSoup, profile_url: str) -> Dict[str, Any]:
        """
        HTML'den profil verilerini çıkar
        
        Args:
            soup: BeautifulSoup objesi
            profile_url (str): Profil URL'i
            
        Returns:
            dict: Çıkarılan profil verileri
        """
        profile_data = {
            'url': profile_url,
            'platform': self._detect_platform(profile_url),
            'username': None,
            'full_name': None,
            'bio': None,
            'profile_picture': None,
            'verification_status': False,
            'followers_count': None,
            'following_count': None,
            'posts_count': None
        }
        
        # Platform bazlı veri çıkarma
        platform = profile_data['platform']
        
        if platform == 'instagram':
            profile_data.update(self._extract_instagram_data(soup))
        elif platform == 'twitter':
            profile_data.update(self._extract_twitter_data(soup))
        elif platform == 'linkedin':
            profile_data.update(self._extract_linkedin_data(soup))
        elif platform == 'facebook':
            profile_data.update(self._extract_facebook_data(soup))
        else:
            # Genel meta tag'lerden veri çıkar
            profile_data.update(self._extract_generic_data(soup))
        
        return profile_data
    
    def _detect_platform(self, url: str) -> str:
        """URL'den platform tespit et"""
        domain = urlparse(url).netloc.lower()
        
        if 'instagram.com' in domain:
            return 'instagram'
        elif 'twitter.com' in domain or 'x.com' in domain:
            return 'twitter'
        elif 'linkedin.com' in domain:
            return 'linkedin'
        elif 'facebook.com' in domain:
            return 'facebook'
        elif 'youtube.com' in domain:
            return 'youtube'
        elif 'tiktok.com' in domain:
            return 'tiktok'
        else:
            return 'unknown'
    
    def _extract_instagram_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Instagram verilerini çıkar"""
        data = {}
        
        # Meta tag'lerden veri çıkar
        title_tag = soup.find('title')
        if title_tag:
            data['full_name'] = title_tag.get_text().strip()
        
        # Open Graph meta tag'leri
        og_title = soup.find('meta', property='og:title')
        if og_title:
            data['full_name'] = og_title.get('content', '')
        
        og_description = soup.find('meta', property='og:description')
        if og_description:
            data['bio'] = og_description.get('content', '')
        
        og_image = soup.find('meta', property='og:image')
        if og_image:
            data['profile_picture'] = og_image.get('content', '')
        
        return data
    
    def _extract_twitter_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Twitter/X verilerini çıkar"""
        data = {}
        
        # Meta tag'lerden veri çıkar
        title_tag = soup.find('title')
        if title_tag:
            data['full_name'] = title_tag.get_text().strip()
        
        # Twitter Card meta tag'leri
        twitter_title = soup.find('meta', property='twitter:title')
        if twitter_title:
            data['full_name'] = twitter_title.get('content', '')
        
        twitter_description = soup.find('meta', property='twitter:description')
        if twitter_description:
            data['bio'] = twitter_description.get('content', '')
        
        twitter_image = soup.find('meta', property='twitter:image')
        if twitter_image:
            data['profile_picture'] = twitter_image.get('content', '')
        
        return data
    
    def _extract_linkedin_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """LinkedIn verilerini çıkar"""
        data = {}
        
        # LinkedIn özel meta tag'leri
        linkedin_title = soup.find('meta', property='og:title')
        if linkedin_title:
            data['full_name'] = linkedin_title.get('content', '')
        
        linkedin_description = soup.find('meta', property='og:description')
        if linkedin_description:
            data['bio'] = linkedin_description.get('content', '')
        
        linkedin_image = soup.find('meta', property='og:image')
        if linkedin_image:
            data['profile_picture'] = linkedin_image.get('content', '')
        
        return data
    
    def _extract_facebook_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Facebook verilerini çıkar"""
        data = {}
        
        # Facebook meta tag'leri
        fb_title = soup.find('meta', property='og:title')
        if fb_title:
            data['full_name'] = fb_title.get('content', '')
        
        fb_description = soup.find('meta', property='og:description')
        if fb_description:
            data['bio'] = fb_description.get('content', '')
        
        fb_image = soup.find('meta', property='og:image')
        if fb_image:
            data['profile_picture'] = fb_image.get('content', '')
        
        return data
    
    def _extract_generic_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Genel meta tag'lerden veri çıkar"""
        data = {}
        
        # Genel meta tag'ler
        title_tag = soup.find('title')
        if title_tag:
            data['full_name'] = title_tag.get_text().strip()
        
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if description_tag:
            data['bio'] = description_tag.get('content', '')
        
        # Open Graph image
        og_image = soup.find('meta', property='og:image')
        if og_image:
            data['profile_picture'] = og_image.get('content', '')
        
        return data
    
    def reverse_image_search(self, image_url: str) -> Dict[str, Any]:
        """
        Google Custom Search API ile ters görsel arama yap
        
        Args:
            image_url (str): Aranacak görsel URL'i
            
        Returns:
            dict: Ters görsel arama sonuçları
        """
        try:
            logger.info(f"Ters görsel arama başlatıldı: {image_url}")
            
            # Google Custom Search API çağrısı
            search_results = self.google_service.cse().list(
                q=image_url,
                cx=self.google_search_engine_id,
                searchType='image',
                num=10  # Maksimum 10 sonuç
            ).execute()
            
            # Sonuçları işle
            reverse_search_data = {
                'image_url': image_url,
                'total_results': search_results.get('searchInformation', {}).get('totalResults', '0'),
                'search_time': search_results.get('searchInformation', {}).get('searchTime', '0'),
                'results': []
            }
            
            # Her sonucu işle
            for item in search_results.get('items', []):
                result = {
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'image_url': item.get('image', {}).get('src', ''),
                    'source': item.get('displayLink', ''),
                    'context_link': item.get('image', {}).get('contextLink', '')
                }
                reverse_search_data['results'].append(result)
            
            logger.info(f"Ters görsel arama tamamlandı: {len(reverse_search_data['results'])} sonuç")
            return reverse_search_data
            
        except HttpError as e:
            logger.error(f"Google API hatası: {str(e)}")
            raise Exception(f"Ters görsel arama başarısız: {str(e)}")
        except Exception as e:
            logger.error(f"Beklenmeyen hata: {str(e)}")
            raise Exception(f"Ters görsel arama hatası: {str(e)}")
    
    def analyze_profile(self, profile_url: str) -> Dict[str, Any]:
        """
        Tam profil analizi yap
        
        Args:
            profile_url (str): Analiz edilecek profil URL'i
            
        Returns:
            dict: Tam analiz sonuçları
        """
        try:
            logger.info(f"Profil analizi başlatıldı: {profile_url}")
            
            # 1. Profil verilerini çek
            profile_data = self.scrape_profile(profile_url)
            
            # 2. Profil resmi varsa ters görsel arama yap
            reverse_search_data = None
            if profile_data.get('profile_picture'):
                try:
                    reverse_search_data = self.reverse_image_search(profile_data['profile_picture'])
                except Exception as e:
                    logger.warning(f"Ters görsel arama başarısız: {str(e)}")
                    reverse_search_data = {'error': str(e)}
            
            # 3. Sonuçları birleştir
            analysis_result = {
                'profile_analysis': profile_data,
                'reverse_image_search': reverse_search_data,
                'analysis_timestamp': int(time.time()),
                'analysis_status': 'completed'
            }
            
            logger.info("Profil analizi başarıyla tamamlandı")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Profil analizi hatası: {str(e)}")
            return {
                'error': str(e),
                'analysis_timestamp': int(time.time()),
                'analysis_status': 'failed'
            }

# Global analyzer instance
analyzer = None

@app.on_event("startup")
async def startup_event():
    """Uygulama başlatıldığında çalışır"""
    global analyzer
    try:
        analyzer = ProfileAnalyzer()
        logger.info("API server başarıyla başlatıldı")
    except Exception as e:
        logger.error(f"API server başlatılamadı: {str(e)}")
        raise

@app.get("/")
async def root():
    """Ana sayfa"""
    return {
        "message": "Sosyal Medya Profil Analiz API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoint": "/analyze"
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "analyzer_ready": analyzer is not None
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_profile_endpoint(request: AnalyzeRequest):
    """
    Sosyal medya profil analizi endpoint'i
    
    Args:
        request: AnalyzeRequest modeli (profile_url içerir)
        
    Returns:
        AnalyzeResponse: Analiz sonuçları
    """
    start_time = time.time()
    
    try:
        # Analyzer'ın hazır olduğunu kontrol et
        if analyzer is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Analyzer henüz hazır değil"
            )
        
        # URL'yi string'e çevir
        profile_url = str(request.profile_url)
        
        logger.info(f"Analiz isteği alındı: {profile_url}")
        
        # Profil analizini gerçekleştir
        analysis_result = analyzer.analyze_profile(profile_url)
        
        processing_time = time.time() - start_time
        
        # Başarılı yanıt
        if analysis_result.get('analysis_status') == 'completed':
            return AnalyzeResponse(
                success=True,
                data=analysis_result,
                error=None,
                timestamp=int(time.time()),
                processing_time=round(processing_time, 2)
            )
        else:
            # Hata durumu
            return AnalyzeResponse(
                success=False,
                data=None,
                error=analysis_result.get('error', 'Bilinmeyen hata'),
                timestamp=int(time.time()),
                processing_time=round(processing_time, 2)
            )
            
    except HTTPException:
        # HTTP exception'ları olduğu gibi fırlat
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Endpoint hatası: {str(e)}")
        
        return AnalyzeResponse(
            success=False,
            data=None,
            error=f"Sunucu hatası: {str(e)}",
            timestamp=int(time.time()),
            processing_time=round(processing_time, 2)
        )

if __name__ == "__main__":
    # Development için direkt çalıştırma
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
