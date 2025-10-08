#!/usr/bin/env python3
"""
Sosyal Medya Profil Analiz Scripti

Bu script, sosyal medya profillerini analiz eder:
1. Scraper API ile profil verilerini çeker
2. Google Custom Search API ile ters görsel arama yapar
3. Sonuçları JSON formatında döndürür

GÜVENLİK: API anahtarları .env dosyasından yüklenir
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

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProfileAnalyzer:
    """Sosyal medya profil analiz sınıfı"""
    
    def __init__(self):
        """API anahtarlarını .env dosyasından yükle"""
        load_dotenv()
        
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
    
    def scrape_profile(self, profile_url):
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
    
    def _extract_profile_data(self, soup, profile_url):
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
    
    def _detect_platform(self, url):
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
    
    def _extract_instagram_data(self, soup):
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
    
    def _extract_twitter_data(self, soup):
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
    
    def _extract_linkedin_data(self, soup):
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
    
    def _extract_facebook_data(self, soup):
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
    
    def _extract_generic_data(self, soup):
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
    
    def reverse_image_search(self, image_url):
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
    
    def analyze_profile(self, profile_url):
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


def main():
    """Ana fonksiyon"""
    print("Sosyal Medya Profil Analiz Scripti")
    print("=" * 50)
    
    # Kullanıcıdan profil URL'i al
    profile_url = input("Analiz edilecek profil URL'ini girin: ").strip()
    
    if not profile_url:
        print("HATA: Geçersiz URL!")
        return
    
    # URL formatını kontrol et
    if not profile_url.startswith(('http://', 'https://')):
        profile_url = 'https://' + profile_url
    
    try:
        # Profil analizini başlat
        analyzer = ProfileAnalyzer()
        result = analyzer.analyze_profile(profile_url)
        
        # Sonuçları JSON olarak yazdır
        print("\nAnaliz Sonuçları:")
        print("=" * 50)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Özet bilgileri yazdır
        if result.get('analysis_status') == 'completed':
            profile = result.get('profile_analysis', {})
            print(f"\nSUCCESS: Analiz Tamamlandı!")
            print(f"Platform: {profile.get('platform', 'Bilinmiyor')}")
            print(f"Isim: {profile.get('full_name', 'Bilinmiyor')}")
            print(f"Bio: {profile.get('bio', 'Yok')[:100]}...")
            
            reverse_search = result.get('reverse_image_search')
            if reverse_search and not reverse_search.get('error'):
                print(f"Ters Gorsel Arama: {len(reverse_search.get('results', []))} sonuc bulundu")
        else:
            print(f"\nERROR: Analiz Basarisiz: {result.get('error', 'Bilinmeyen hata')}")
    
    except Exception as e:
        print(f"\nHATA: {str(e)}")
        logger.error(f"Ana fonksiyon hatası: {str(e)}")


if __name__ == "__main__":
    main()
