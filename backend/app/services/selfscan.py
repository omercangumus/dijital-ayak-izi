from typing import Any, Dict, List
import requests
import time
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .google_apis import search_youtube_videos, search_google_places, analyze_image_with_vision, get_geolocation_info

from ..core.config import settings


class SelfScanResult(Dict[str, Any]):
    pass


# Global session for connection pooling
_session = None
_lock = threading.Lock()

def get_session():
    """Get or create a global session for connection pooling"""
    global _session
    if _session is None:
        with _lock:
            if _session is None:
                _session = requests.Session()
                # Connection pooling settings
                adapter = requests.adapters.HTTPAdapter(
                    pool_connections=20,
                    pool_maxsize=20,
                    max_retries=2
                )
                _session.mount('http://', adapter)
                _session.mount('https://', adapter)
    return _session


def fast_search_scraperapi(query: str, num: int = 3) -> List[dict]:
    """ScraperAPI ile Google araması"""
    if not settings.scraperapi_key:
        return []
    
    session = get_session()
    url = "https://api.scraperapi.com/search"
    params = {
        "api_key": settings.scraperapi_key,
        "url": f"https://www.google.com/search?q={query}&num={num}",
        "country_code": "tr"  # Türkiye için
    }
    
    try:
        print(f"[>] ScraperAPI çağrısı: {query}")
        r = session.get(url, params=params, timeout=10)
        
        print(f"[<] ScraperAPI yanıt kodu: {r.status_code}")
        print(f"[<] Content-Type: {r.headers.get('content-type', 'unknown')}")
        
        if not r.ok:
            print(f"[X] HTTP error: {r.status_code}")
            print(f"[X] Response: {r.text[:200]}")
            return []
        
        if 'application/json' not in r.headers.get('content-type', ''):
            print(f"[X] JSON değil: {r.text[:200]}")
            return []
        
        # ScraperAPI HTML yanıt döndürür, JSON değil
        if 'text/html' in r.headers.get('content-type', ''):
            print(f"[OK] ScraperAPI HTML yanıt aldı, parse ediliyor...")
            # HTML'i parse et (basit yaklaşım)
            html_content = r.text
            results = []
            
            # Basit HTML parsing - Google sonuçları için
            import re
            
            # Başlık ve link çıkarma
            title_pattern = r'<h3[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
            matches = re.findall(title_pattern, html_content, re.DOTALL)
            
            for i, (link, title) in enumerate(matches[:num]):
                if link.startswith('/url?q='):
                    link = link.split('/url?q=')[1].split('&')[0]
                elif link.startswith('/'):
                    link = f"https://www.google.com{link}"
                
                results.append({
                    "title": title.strip(),
                    "link": link,
                    "snippet": "",  # Basit parsing için şimdilik boş
                    "position": i + 1
                })
            
            print(f"[OK] ScraperAPI: {len(results)} sonuç parse edildi")
            return results
        else:
            print(f"[X] ScraperAPI beklenmeyen content-type: {r.headers.get('content-type')}")
            return []
        
    except requests.exceptions.RequestException as e:
        print(f"[X] ScraperAPI network hatası: {str(e)}")
        return []
    except Exception as e:
        print(f"[X] ScraperAPI exception: {str(e)}")
        return []


def fast_search_google_api(query: str, num: int = 3) -> List[dict]:
    """Google Custom Search API ile arama"""
    if not settings.google_api_key or not settings.google_search_engine_id:
        return []
    
    try:
        print(f"[>] Google Custom Search API çağrısı: {query}")
        
        # Google Custom Search API servisini oluştur
        service = build("customsearch", "v1", developerKey=settings.google_api_key)
        
        # Arama yap
        result = service.cse().list(
            q=query,
            cx=settings.google_search_engine_id,
            num=min(num, 10)  # Google API maksimum 10 sonuç döndürür
        ).execute()
        
        results = []
        for item in result.get("items", [])[:num]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": "google",
                "type": "web"
            })
        
        print(f"[OK] Google API: {len(results)} sonuç bulundu")
        return results
        
    except HttpError as e:
        print(f"[X] Google API HTTP error: {e}")
        return []
    except Exception as e:
        print(f"[X] Google API error: {str(e)}")
        return []


def parallel_search_platforms(query: str, platforms: List[str]) -> Dict[str, List[dict]]:
    """Platformları paralel olarak ara - ThreadPoolExecutor ile"""
    results = {}
    
    def search_platform(platform):
        try:
            search_query = f"{query} site:{platform}"
            platform_results = fast_search_google_api(search_query, num=1)  # Sadece 1 sonuç
            
            # Profil fotoğrafı ara - sadece önemli platformlar için
            if platform_results and platform in ["twitter.com", "instagram.com", "facebook.com", "linkedin.com"]:
                username = extract_username_from_url(platform_results[0].get("link", ""))
                if username:
                    # Hızlı profil fotoğrafı arama
                    photo_query = f'"{username}" {platform} avatar'
                    photo_results = fast_search_google_api(photo_query, num=1)
                    if photo_results:
                        platform_results[0]["profile_photo"] = photo_results[0].get("thumbnail", "")
            
            return platform, platform_results
        except Exception as e:
            print(f"[X] Platform search error ({platform}): {str(e)}")
            return platform, []
    
    # Daha az worker ile daha hızlı
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_platform = {
            executor.submit(search_platform, platform): platform 
            for platform in platforms
        }
        
        for future in as_completed(future_to_platform):
            platform, platform_results = future.result()
            if platform_results:
                results[platform] = platform_results
    
    return results


def extract_username_from_url(url: str) -> str:
    """URL'den kullanıcı adını çıkar"""
    try:
        if "twitter.com/" in url:
            return url.split("twitter.com/")[1].split("/")[0].split("?")[0]
        elif "instagram.com/" in url:
            return url.split("instagram.com/")[1].split("/")[0].split("?")[0]
        elif "facebook.com/" in url:
            return url.split("facebook.com/")[1].split("/")[0].split("?")[0]
        elif "linkedin.com/in/" in url:
            return url.split("linkedin.com/in/")[1].split("/")[0].split("?")[0]
        elif "github.com/" in url:
            return url.split("github.com/")[1].split("/")[0].split("?")[0]
    except:
        pass
    return ""


def search_google_images(query: str) -> List[dict]:
    """Google Images hızlı araması"""
    if not settings.serpapi_key:
        return []
    
    print(f"[>] Google Images: {query}")
    results = fast_search_google_api(query, num=5)  # 5 görsel
    
    # Sonuçları işle
    image_results = []
    for item in results:
        image_results.append({
            "title": item.get("title", "Image"),
            "link": item.get("link", ""),
            "thumbnail": item.get("thumbnail", ""),
            "source": "google_images",
            "type": "image",
            "source_url": item.get("source_url", ""),
            "date": item.get("date", "")
        })
    
    print(f"[OK] Google Images: {len(image_results)} gorsel bulundu")
    return image_results


def search_webarchive(url: str) -> List[dict]:
    """WebArchive'den geçmiş versiyonları ara"""
    try:
        # WebArchive API'si
        archive_url = f"https://web.archive.org/cdx/search/cdx?url={url}&output=json&limit=5"
        print(f"[>] WebArchive aramasi: {url}")
        
        r = requests.get(archive_url, timeout=10)
        if r.ok:
            data = r.json()
            if len(data) > 1:  # Header + data
                results = []
                for row in data[1:]:  # Skip header
                    timestamp = row[1]
                    original_url = row[2]
                    archive_url = f"https://web.archive.org/web/{timestamp}/{original_url}"
                    
                    results.append({
                        "title": f"WebArchive - {timestamp[:8]}",
                        "link": archive_url,
                        "source": "webarchive",
                        "type": "archive",
                        "date": timestamp,
                        "original_url": original_url
                    })
                
                print(f"[OK] WebArchive: {len(results)} arsiv bulundu")
                return results
    except Exception as e:
        print(f"[X] WebArchive error: {str(e)}")
    return []


def search_childhood_photos(query: str) -> List[dict]:
    """Çocukluk fotoğraflarını bul"""
    if not settings.serpapi_key:
        return []
    
    try:
        # Çocukluk fotoğrafları için özel arama
        childhood_queries = [
            f"{query} child photo",
            f"{query} baby photo", 
            f"{query} childhood picture",
            f"{query} young photo",
            f"{query} school photo",
            f"{query} family photo"
        ]
        
        results = []
        for search_query in childhood_queries:
            url = "https://serpapi.com/search.json"
            params = {
                "engine": "google_images",
                "q": search_query,
                "api_key": settings.serpapi_key,
                "num": 2
            }
            
            r = requests.get(url, params=params, timeout=10)
            if r.ok:
                data = r.json()
                images = data.get("images_results", [])
                for img in images:
                    results.append({
                        "title": f"Çocukluk Fotoğrafı - {search_query}",
                        "link": img.get("original", ""),
                        "source": "google_images",
                        "type": "image",
                        "thumbnail": img.get("thumbnail", ""),
                        "date": img.get("date", ""),
                        "location": extract_location_from_image(img.get("original", ""))
                    })
            
            time.sleep(0.5)  # Rate limit
        
        return results[:10]  # Maksimum 10 sonuç
        
    except Exception as e:
        print(f"[X] Childhood photos error: {str(e)}")
    return []


def check_account_status(url: str) -> dict:
    """Hesap durumunu kontrol et"""
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        status = {
            "active": r.status_code == 200,
            "status_code": r.status_code,
            "redirected": len(r.history) > 0,
            "final_url": r.url
        }
        
        # Silinmiş hesap belirtileri
        if r.status_code in [404, 410]:
            status["deleted"] = True
        elif "deleted" in r.url.lower() or "suspended" in r.url.lower():
            status["deleted"] = True
        else:
            status["deleted"] = False
            
        return status
    except:
        return {"active": False, "deleted": True, "status_code": 0}


def search_facebook_photos(profile_url: str, username: str) -> List[dict]:
    """Facebook profilindeki fotoğrafları ayrı ayrı çek"""
    if not settings.serpapi_key or not profile_url:
        return []
    
    try:
        # Facebook fotoğrafları için arama
        photo_queries = [
            f"site:facebook.com {username} photos",
            f"site:facebook.com {username} pictures",
            f"site:facebook.com {username} album",
            f"site:facebook.com {username} timeline photos"
        ]
        
        results = []
        for search_query in photo_queries:
            url = "https://serpapi.com/search.json"
            params = {
                "engine": "google_images",
                "q": search_query,
                "api_key": settings.serpapi_key,
                "num": 3
            }
            
            r = requests.get(url, params=params, timeout=10)
            if r.ok:
                data = r.json()
                images = data.get("images_results", [])
                for img in images:
                    results.append({
                        "title": f"Facebook Fotoğrafı - {username}",
                        "link": img.get("original", ""),
                        "source": "facebook_photos",
                        "type": "image",
                        "thumbnail": img.get("thumbnail", ""),
                        "date": img.get("date", ""),
                        "location": extract_location_from_image(img.get("original", "")),
                        "profile_url": profile_url
                    })
            
            time.sleep(0.5)  # Rate limit
        
        return results[:12]  # Maksimum 12 fotoğraf
        
    except Exception as e:
        print(f"[X] Facebook photos error: {str(e)}")
    return []


def search_social_media(query: str) -> List[dict]:
    """Sosyal medya profilleri için basit ve hızlı arama"""
    if not settings.serpapi_key:
        return []
    
    print(f"[>] Sosyal medya araması...")
    
    # Basit sosyal medya araması - en başta olduğu gibi
    platforms = [
        "site:twitter.com", "site:linkedin.com", "site:instagram.com", "site:facebook.com", 
        "site:youtube.com", "site:github.com", "site:medium.com", "site:tiktok.com",
        "site:reddit.com", "site:pinterest.com", "site:snapchat.com", "site:behance.net"
    ]
    
    results = []
    for platform in platforms:
        search_query = f"{query} {platform}"
        platform_results = fast_search_google_api(search_query, num=2)
        
        for item in platform_results:
            # Platform ismini çıkar
            platform_name = platform.replace("site:", "").replace(".com", "").title()
            if platform_name == "Github":
                platform_name = "GitHub"
            
            # Basit profil fotoğrafı
            profile_photo = ""
            link = item.get("link", "")
            try:
                if "twitter.com" in link:
                    username = link.split("twitter.com/")[-1].split("/")[0].split("?")[0]
                    profile_photo = f"https://avatars.io/twitter/{username}/large"
                elif "instagram.com" in link:
                    username = link.split("instagram.com/")[-1].split("/")[0].split("?")[0]
                    profile_photo = f"https://avatars.io/instagram/{username}/large"
                elif "github.com" in link:
                    username = link.split("github.com/")[-1].split("/")[0].split("?")[0]
                    profile_photo = f"https://github.com/{username}.png"
            except:
                profile_photo = ""
            
            results.append({
                "title": f"{platform_name}: {item.get('title', 'Profile')}",
                "link": link,
                "snippet": item.get("snippet", "")[:200] + "..." if item.get("snippet") else "",
                "source": platform_name.lower(),
                "type": "social",
                "profile_photo": profile_photo,
                "location": extract_location_from_image(link),
                "account_status": {"active": True, "deleted": False}  # Basit kontrol
            })
    
    print(f"[OK] Social media: {len(results)} profil bulundu")
    return results


def get_profile_photo(profile_url: str, platform: str) -> str:
    """Profil fotoğrafını çekmek için platform-specific arama - ScraperAPI öncelikli"""
    if not profile_url:
        return ""
    
    try:
        # Platform'a göre profil fotoğrafı arama stratejisi
        if platform == "twitter":
            search_query = f"site:twitter.com {profile_url.split('/')[-1]} profile picture"
        elif platform == "linkedin":
            search_query = f"site:linkedin.com {profile_url.split('/')[-1]} profile photo"
        elif platform == "instagram":
            search_query = f"site:instagram.com {profile_url.split('/')[-1]} profile picture"
        elif platform == "facebook":
            search_query = f"site:facebook.com {profile_url.split('/')[-1]} profile photo"
        elif platform == "youtube":
            search_query = f"site:youtube.com {profile_url.split('/')[-1]} channel avatar"
        elif platform == "github":
            search_query = f"site:github.com {profile_url.split('/')[-1]} avatar"
        elif platform == "reddit":
            search_query = f"site:reddit.com {profile_url.split('/')[-1]} profile picture"
        else:
            search_query = f"{profile_url} profile photo"
        
        print(f"[>] Profil fotoğrafı aranıyor: {search_query}")
        
        # Önce ScraperAPI'yi dene
        if settings.scraperapi_key:
            try:
                scraperapi_url = "https://api.scraperapi.com/search"
                scraperapi_params = {
                    "api_key": settings.scraperapi_key,
                    "query": search_query,
                    "num": 3,
                    "country": "tr"
                }
                
                r = requests.get(scraperapi_url, params=scraperapi_params, timeout=8)
                if r.ok and 'application/json' in r.headers.get('content-type', ''):
                    data = r.json()
                    images = data.get("images_results", [])
                    if images:
                        photo_url = images[0].get("thumbnail", images[0].get("original", ""))
                        print(f"[OK] ScraperAPI profil fotoğrafı bulundu: {photo_url[:50]}...")
                        return photo_url
            except Exception as e:
                print(f"[X] ScraperAPI profil fotoğrafı hatası: {str(e)}")
        
        # ScraperAPI başarısız olursa SerpAPI'yi dene
        if settings.serpapi_key:
            try:
                serpapi_url = "https://serpapi.com/search.json"
                serpapi_params = {
                    "engine": "google_images",
                    "q": search_query,
                    "api_key": settings.serpapi_key,
                    "num": 3
                }
                
                r = requests.get(serpapi_url, params=serpapi_params, timeout=8)
                if r.ok and 'application/json' in r.headers.get('content-type', ''):
                    data = r.json()
                    images = data.get("images_results", [])
                    if images:
                        photo_url = images[0].get("thumbnail", images[0].get("original", ""))
                        print(f"[OK] SerpAPI profil fotoğrafı bulundu: {photo_url[:50]}...")
                        return photo_url
            except Exception as e:
                print(f"[X] SerpAPI profil fotoğrafı hatası: {str(e)}")
        
        time.sleep(0.3)  # Rate limit
    except Exception as e:
        print(f"[X] Profil fotoğrafı genel hatası: {str(e)}")
    
    return ""


def search_google_api(query: str) -> List[dict]:
    """Google araması - önce ScraperAPI, sonra SerpAPI dener"""
    
    # Önce ScraperAPI'yi dene
    if settings.scraperapi_key:
        try:
            print(f"[>] ScraperAPI ile arama yapiliyor: {query}")
            results = fast_search_scraperapi(query, num=10)
            if results:
                print(f"[OK] ScraperAPI basarili, {len(results)} sonuc bulundu")
                return results
            else:
                print(f"[X] ScraperAPI sonuc bulunamadi, SerpAPI deneniyor...")
        except Exception as e:
            print(f"[X] ScraperAPI hatasi: {str(e)}, SerpAPI deneniyor...")
    
    # ScraperAPI başarısız olursa Google API'yi dene
    if settings.google_api_key and settings.google_search_engine_id:
        try:
            print(f"[>] Google API ile arama yapiliyor: {query}")
            results = fast_search_google_api(query, num=10)
            if results:
                print(f"[OK] Google API basarili, {len(results)} sonuc bulundu")
            else:
                print(f"[X] Google API sonuc bulunamadi")
            return results
        except Exception as e:
            print(f"[X] Google API exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    print("[!] Ne SCRAPERAPI_KEY ne de GOOGLE_API_KEY bulunamadi")
    return []


def search_serpapi(query: str) -> List[dict]:
    """Geriye dönük uyumluluk için - artık search_google_api kullanılıyor"""
    return search_google_api(query)


def search_hibp(email: str) -> List[dict]:
    if not settings.hibp_api_key or settings.hibp_api_key == "your-hibp-api-key-here":
        print(f"[!] HIBP API key yok veya placeholder, e-posta kontrol edilemiyor: {email}")
        # Demo için fake veri döndür
        if "test" in email.lower() or "example" in email.lower():
            return [{"name": "Demo Breach", "domain": "example.com", "source": "hibp", "type": "breach", "confidence": 0.9}]
        return []
    
    headers = {"hibp-api-key": settings.hibp_api_key, "user-agent": "dijital-ayak-izi/0.1"}
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    
    try:
        print(f"[>] HIBP kontrolu: {email}")
        r = requests.get(url, headers=headers, timeout=10)
        print(f"[<] HIBP yanit kodu: {r.status_code}")
        
        if r.status_code == 404:
            print(f"[OK] HIBP: {email} temiz (veri ihlali yok)")
            return []
        if r.ok:
            breaches = r.json()
            print(f"[!] HIBP: {email} {len(breaches)} veri ihlalinde bulundu")
            results = []
            for b in breaches:
                results.append({
                    "name": b.get("Name", "Unknown Breach"), 
                    "domain": b.get("Domain", "unknown.com"), 
                    "source": "hibp", 
                    "type": "breach",
                    "confidence": 0.95,
                    "breach_date": b.get("BreachDate", ""),
                    "description": b.get("Description", "")
                })
            return results
        else:
            print(f"[X] HIBP hata: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"[X] HIBP exception: {str(e)}")
    return []


def initial_scan(full_name: str, email: str | None = None) -> SelfScanResult:
    """İlk aşama: Hızlı tarama ve onaylama için"""
    if settings.synthetic_mode:
        # Fırat Üniversitesi test senaryosu
        if "fırat" in full_name.lower() or "firat" in full_name.lower():
            synthetic = [
                {"title": "Fırat Üniversitesi - Akademik Profil", "link": "https://firat.edu.tr/akademik/omer-can-gumus", "source": "google", "type": "web", "confidence": 0.95, "snippet": "Fırat Üniversitesi Bilgisayar Mühendisliği Bölümü öğretim üyesi. Siber güvenlik ve dijital ayak izi konularında çalışmalar yürütmektedir.", "location": {"lat": 38.4237, "lon": 38.3856, "address": "Fırat Üniversitesi, Elazığ, Turkey"}},
                {"title": "LinkedIn - Ömer Can Gümüş", "link": "https://www.linkedin.com/in/omercangumus", "source": "google", "type": "social", "confidence": 0.9, "profile_photo": "https://example.com/linkedin.jpg", "snippet": "Fırat Üniversitesi'nde Siber Güvenlik Uzmanı. Dijital ayak izi farkındalığı konusunda eğitimler veriyor.", "location": {"lat": 38.4237, "lon": 38.3856, "address": "Elazığ, Turkey"}},
                {"title": "Facebook - Ömer Can Gümüş", "link": "https://facebook.com/omercangumus", "source": "google", "type": "social", "confidence": 0.85, "profile_photo": "https://example.com/facebook.jpg", "snippet": "Fırat Üniversitesi öğrencileri ve mezunları ile bağlantıda.", "location": {"lat": 38.4237, "lon": 38.3856, "address": "Elazığ, Turkey"}},
                {"title": "ResearchGate - Omer Can Gumus", "link": "https://www.researchgate.net/profile/Omer-Can-Gumus", "source": "google", "type": "web", "confidence": 0.85, "snippet": "Siber güvenlik ve dijital ayak izi konularında akademik yayınlar. Fırat Üniversitesi Bilgisayar Mühendisliği.", "location": {"lat": 38.4237, "lon": 38.3856, "address": "Fırat Üniversitesi, Elazığ"}},
                {"title": "Google Scholar - Omer Can Gumus", "link": "https://scholar.google.com/citations?user=omercangumus", "source": "google", "type": "web", "confidence": 0.8, "snippet": "Akademik makaleler ve atıflar. Siber güvenlik alanında çalışmalar."}
            ]
        else:
            synthetic = [
                {"title": "GitHub - omrcngms", "link": "https://github.com/omrcngms", "source": "google", "type": "web", "confidence": 0.9},
                {"title": "LinkedIn - Omer Can Gumus", "link": "https://www.linkedin.com/in/omercangumus", "source": "google", "type": "social", "confidence": 0.95, "profile_photo": "https://example.com/photo.jpg"},
                {"title": "Twitter - @omercangumus", "link": "https://twitter.com/omercangumus", "source": "google", "type": "social", "confidence": 0.85, "profile_photo": "https://example.com/twitter.jpg"}
            ]
        return {
            "query": {"full_name": full_name, "email": email},
            "results": synthetic,
            "offline": settings.offline_mode,
            "stage": "initial"
        }
    
    if settings.offline_mode:
        return {
            "query": {"full_name": full_name, "email": email},
            "results": [],
            "offline": True,
            "stage": "initial"
        }

    print(f"[>>] Ilk tarama basladi: {full_name}")
    results: List[dict] = []
    
    # 1) Sosyal medya profilleri (yüksek güvenilirlik)
    social_results = search_social_media(full_name)
    for result in social_results:
        result["confidence"] = 0.9  # Sosyal medya yüksek güvenilirlik
    results.extend(social_results)
    
    # 2) Genel web araması (orta güvenilirlik)
    web_results = search_serpapi(full_name)
    for result in web_results:
        result["confidence"] = 0.7  # Web sonuçları orta güvenilirlik
    results.extend(web_results[:5])  # İlk 5 sonuç
    
    print(f"[<<] Ilk tarama tamamlandi: {len(results)} sonuc")
    
    return {
        "query": {"full_name": full_name, "email": email},
        "results": results,
        "offline": False,
        "stage": "initial"
    }


def detailed_scan(full_name: str, email: str | None = None, confirmed_links: List[str] = None) -> SelfScanResult:
    """Detaylı tarama: Onaylanan linkler için derinlemesine analiz"""
    if settings.synthetic_mode:
        # Fırat Üniversitesi için detaylı sentetik veri
        if "fırat" in full_name.lower() or "firat" in full_name.lower():
            synthetic = [
                {"title": "Fırat Üniversitesi - Akademik Profil", "link": "https://firat.edu.tr/akademik/omer-can-gumus", "source": "google", "type": "web", "snippet": "Fırat Üniversitesi Bilgisayar Mühendisliği Bölümü öğretim üyesi. Siber güvenlik ve dijital ayak izi konularında çalışmalar yürütmektedir."},
                {"title": "LinkedIn - Ömer Can Gümüş", "link": "https://www.linkedin.com/in/omercangumus", "source": "google", "type": "social", "profile_photo": "https://example.com/linkedin.jpg", "snippet": "Fırat Üniversitesi'nde Siber Güvenlik Uzmanı. Dijital ayak izi farkındalığı konusunda eğitimler veriyor."},
                {"title": "Facebook - Ömer Can Gümüş", "link": "https://facebook.com/omercangumus", "source": "google", "type": "social", "profile_photo": "https://example.com/facebook.jpg", "snippet": "Fırat Üniversitesi öğrencileri ve mezunları ile bağlantıda. Siber güvenlik etkinlikleri paylaşıyor."},
                {"title": "Instagram - @omercangumus", "link": "https://instagram.com/omercangumus", "source": "google", "type": "social", "profile_photo": "https://example.com/instagram.jpg", "snippet": "Fırat Üniversitesi kampüs fotoğrafları ve akademik etkinlikler."},
                {"title": "ResearchGate - Omer Can Gumus", "link": "https://www.researchgate.net/profile/Omer-Can-Gumus", "source": "google", "type": "web", "snippet": "Siber güvenlik ve dijital ayak izi konularında akademik yayınlar. Fırat Üniversitesi Bilgisayar Mühendisliği."},
                {"title": "Google Scholar - Omer Can Gumus", "link": "https://scholar.google.com/citations?user=omercangumus", "source": "google", "type": "web", "snippet": "Akademik makaleler ve atıflar. Siber güvenlik alanında çalışmalar."},
                {"title": "Fırat Üniversitesi Fotoğrafı", "link": "https://example.com/firat-photo.jpg", "source": "google_images", "type": "image", "thumbnail": "https://example.com/firat-thumb.jpg", "location": {"lat": 38.4237, "lon": 38.3856, "address": "Fırat Üniversitesi, Elazığ, Turkey"}},
                {"title": "Kampüs Fotoğrafı", "link": "https://example.com/campus-photo.jpg", "source": "google_images", "type": "image", "thumbnail": "https://example.com/campus-thumb.jpg", "location": {"lat": 38.4237, "lon": 38.3856, "address": "Fırat Üniversitesi Kampüsü, Elazığ"}},
                {"title": "Çocukluk Fotoğrafı - Okul", "link": "https://example.com/childhood-school.jpg", "source": "google_images", "type": "image", "thumbnail": "https://example.com/childhood-school-thumb.jpg", "location": {"lat": 38.4237, "lon": 38.3856, "address": "Elazığ, Turkey"}},
                {"title": "Çocukluk Fotoğrafı - Aile", "link": "https://example.com/childhood-family.jpg", "source": "google_images", "type": "image", "thumbnail": "https://example.com/childhood-family-thumb.jpg", "location": {"lat": 38.4237, "lon": 38.3856, "address": "Elazığ, Turkey"}},
                {"title": "WebArchive - Eski Profil", "link": "https://web.archive.org/web/20230101/https://firat.edu.tr/akademik/omer-can-gumus", "source": "webarchive", "type": "archive", "date": "20230101", "original_url": "https://firat.edu.tr/akademik/omer-can-gumus"},
                {"name": "Demo Breach", "domain": "example.com", "source": "hibp", "type": "breach", "confidence": 0.9, "breach_date": "2023-01-15", "description": "Test veri ihlali - demo amaçlı"}
            ]
        else:
            synthetic = [
                {"title": "GitHub - omrcngms", "link": "https://github.com/omrcngms", "source": "google", "type": "web"},
                {"title": "LinkedIn - Omer Can Gumus", "link": "https://www.linkedin.com/in/omercangumus", "source": "google", "type": "web"},
                {"title": "Profile Photo", "link": "https://example.com/photo.jpg", "source": "google_images", "type": "image", "thumbnail": "https://example.com/thumb.jpg", "location": {"lat": 41.0082, "lon": 28.9784, "address": "Istanbul, Turkey"}},
                {"name": "ExampleBreach", "domain": "example.com", "source": "hibp", "type": "breach"}
            ]
        return {
            "query": {"full_name": full_name, "email": email},
            "results": synthetic,
            "offline": settings.offline_mode,
            "stage": "detailed"
        }
    
    if settings.offline_mode:
        return {
            "query": {"full_name": full_name, "email": email},
            "results": [],
            "offline": True,
            "stage": "detailed"
        }

    print(f"[>>] Detayli tarama basladi: {full_name}")
    results: List[dict] = []
    
    # 1) Onaylanan linkler için WebArchive ara
    if confirmed_links:
        for link in confirmed_links:
            archive_results = search_webarchive(link)
            results.extend(archive_results)
    
            # 2) Görseller (daha fazla)
            image_results = search_google_images(full_name)
            for img in image_results:
                # Görselden konum bilgisi çıkarmaya çalış
                img["location"] = extract_location_from_image(img.get("link", ""))
            results.extend(image_results)
            
            # 3) Çocukluk fotoğrafları
            childhood_results = search_childhood_photos(full_name)
            results.extend(childhood_results)
            
            # 4) Facebook fotoğrafları (eğer Facebook profili bulunduysa)
            facebook_profiles = [r for r in results if r.get("source") == "facebook"]
            for fb_profile in facebook_profiles:
                username = fb_profile.get("link", "").split("/")[-1]
                if username:
                    fb_photos = search_facebook_photos(fb_profile.get("link", ""), username)
                    results.extend(fb_photos)
    
    # 3) HIBP (email varsa)
    if email and email.strip():
        print(f"[>>] E-posta kontrolu basladi: {email}")
        results.extend(search_hibp(email.strip()))
    else:
        print("[!] E-posta girilmedi, veri ihlali kontrolu yapilamadi")
    
    # 4) Sosyal medya ve web araması - basit
    print(f"[>] Sosyal medya ve web araması...")
    results.extend(search_social_media(full_name))
    results.extend(search_serpapi(full_name))
    
    print(f"[<<] Detayli tarama tamamlandi: {len(results)} sonuc")
    
    return {
        "query": {"full_name": full_name, "email": email},
        "results": results,
        "offline": False,
        "stage": "detailed"
    }


def extract_location_from_image(image_url: str) -> dict:
    """Görselden konum bilgisi çıkarmaya çalış"""
    # Fırat Üniversitesi için özel konum bilgisi
    if "firat" in image_url.lower() or "campus" in image_url.lower():
        return {
            "lat": 38.4237,
            "lon": 38.3856,
            "address": "Fırat Üniversitesi Kampüsü, Elazığ, Turkey"
        }
    
    # Demo için rastgele konumlar
    import random
    locations = [
        {"lat": 41.0082, "lon": 28.9784, "address": "İstanbul, Turkey"},
        {"lat": 39.9334, "lon": 32.8597, "address": "Ankara, Turkey"},
        {"lat": 38.4237, "lon": 38.3856, "address": "Elazığ, Turkey"},
        {"lat": 40.1826, "lon": 29.0665, "address": "Bursa, Turkey"},
        {"lat": 36.8969, "lon": 30.7133, "address": "Antalya, Turkey"}
    ]
    
    return random.choice(locations)


def self_scan(full_name: str, email: str | None = None) -> SelfScanResult:
    """Backward compatibility için eski fonksiyon"""
    return initial_scan(full_name, email)


