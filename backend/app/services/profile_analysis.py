"""
Profil Analiz Motoru - Etik OSINT Araçları
Bu modül, etik ve yasal sınırlar içinde profil analizi yapar.
"""

import requests
import time
import re
import hashlib
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from ..core.config import settings


class ProfileAnalysisEngine:
    """Ana profil analiz motoru sınıfı"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.platforms = self._load_platform_list()
        self.rate_limits = {}
        self.lock = threading.Lock()
    
    def _load_platform_list(self) -> List[Dict[str, str]]:
        """50+ popüler platform listesini yükle"""
        return [
            {"name": "GitHub", "url": "https://github.com/{username}", "check_url": "https://github.com/{username}"},
            {"name": "Twitter", "url": "https://twitter.com/{username}", "check_url": "https://twitter.com/{username}"},
            {"name": "LinkedIn", "url": "https://linkedin.com/in/{username}", "check_url": "https://linkedin.com/in/{username}"},
            {"name": "Instagram", "url": "https://instagram.com/{username}", "check_url": "https://instagram.com/{username}"},
            {"name": "Facebook", "url": "https://facebook.com/{username}", "check_url": "https://facebook.com/{username}"},
            {"name": "YouTube", "url": "https://youtube.com/c/{username}", "check_url": "https://youtube.com/c/{username}"},
            {"name": "Reddit", "url": "https://reddit.com/u/{username}", "check_url": "https://reddit.com/u/{username}"},
            {"name": "TikTok", "url": "https://tiktok.com/@{username}", "check_url": "https://tiktok.com/@{username}"},
            {"name": "Pinterest", "url": "https://pinterest.com/{username}", "check_url": "https://pinterest.com/{username}"},
            {"name": "Snapchat", "url": "https://snapchat.com/add/{username}", "check_url": "https://snapchat.com/add/{username}"},
            {"name": "Medium", "url": "https://medium.com/@{username}", "check_url": "https://medium.com/@{username}"},
            {"name": "Dev.to", "url": "https://dev.to/{username}", "check_url": "https://dev.to/{username}"},
            {"name": "Behance", "url": "https://behance.net/{username}", "check_url": "https://behance.net/{username}"},
            {"name": "Dribbble", "url": "https://dribbble.com/{username}", "check_url": "https://dribbble.com/{username}"},
            {"name": "Steam", "url": "https://steamcommunity.com/id/{username}", "check_url": "https://steamcommunity.com/id/{username}"},
            {"name": "Discord", "url": "https://discord.com/users/{username}", "check_url": "https://discord.com/users/{username}"},
            {"name": "Telegram", "url": "https://t.me/{username}", "check_url": "https://t.me/{username}"},
            {"name": "Twitch", "url": "https://twitch.tv/{username}", "check_url": "https://twitch.tv/{username}"},
            {"name": "Vimeo", "url": "https://vimeo.com/{username}", "check_url": "https://vimeo.com/{username}"},
            {"name": "SoundCloud", "url": "https://soundcloud.com/{username}", "check_url": "https://soundcloud.com/{username}"},
            {"name": "Spotify", "url": "https://open.spotify.com/user/{username}", "check_url": "https://open.spotify.com/user/{username}"},
            {"name": "Last.fm", "url": "https://last.fm/user/{username}", "check_url": "https://last.fm/user/{username}"},
            {"name": "Flickr", "url": "https://flickr.com/photos/{username}", "check_url": "https://flickr.com/photos/{username}"},
            {"name": "500px", "url": "https://500px.com/{username}", "check_url": "https://500px.com/{username}"},
            {"name": "DeviantArt", "url": "https://deviantart.com/{username}", "check_url": "https://deviantart.com/{username}"},
            {"name": "ArtStation", "url": "https://artstation.com/{username}", "check_url": "https://artstation.com/{username}"},
            {"name": "Codepen", "url": "https://codepen.io/{username}", "check_url": "https://codepen.io/{username}"},
            {"name": "Stack Overflow", "url": "https://stackoverflow.com/users/{username}", "check_url": "https://stackoverflow.com/users/{username}"},
            {"name": "GitLab", "url": "https://gitlab.com/{username}", "check_url": "https://gitlab.com/{username}"},
            {"name": "Bitbucket", "url": "https://bitbucket.org/{username}", "check_url": "https://bitbucket.org/{username}"},
            {"name": "Keybase", "url": "https://keybase.io/{username}", "check_url": "https://keybase.io/{username}"},
            {"name": "HackerNews", "url": "https://news.ycombinator.com/user?id={username}", "check_url": "https://news.ycombinator.com/user?id={username}"},
            {"name": "Product Hunt", "url": "https://producthunt.com/@{username}", "check_url": "https://producthunt.com/@{username}"},
            {"name": "AngelList", "url": "https://angel.co/{username}", "check_url": "https://angel.co/{username}"},
            {"name": "Crunchbase", "url": "https://crunchbase.com/person/{username}", "check_url": "https://crunchbase.com/person/{username}"},
            {"name": "SlideShare", "url": "https://slideshare.net/{username}", "check_url": "https://slideshare.net/{username}"},
            {"name": "Speaker Deck", "url": "https://speakerdeck.com/{username}", "check_url": "https://speakerdeck.com/{username}"},
            {"name": "Vimeo", "url": "https://vimeo.com/{username}", "check_url": "https://vimeo.com/{username}"},
            {"name": "Mixcloud", "url": "https://mixcloud.com/{username}", "check_url": "https://mixcloud.com/{username}"},
            {"name": "Goodreads", "url": "https://goodreads.com/user/show/{username}", "check_url": "https://goodreads.com/user/show/{username}"},
            {"name": "Letterboxd", "url": "https://letterboxd.com/{username}", "check_url": "https://letterboxd.com/{username}"},
            {"name": "IMDb", "url": "https://imdb.com/name/{username}", "check_url": "https://imdb.com/name/{username}"},
            {"name": "ResearchGate", "url": "https://researchgate.net/profile/{username}", "check_url": "https://researchgate.net/profile/{username}"},
            {"name": "Academia", "url": "https://academia.edu/{username}", "check_url": "https://academia.edu/{username}"},
            {"name": "ORCID", "url": "https://orcid.org/{username}", "check_url": "https://orcid.org/{username}"},
            {"name": "Google Scholar", "url": "https://scholar.google.com/citations?user={username}", "check_url": "https://scholar.google.com/citations?user={username}"},
            {"name": "Mendeley", "url": "https://mendeley.com/profiles/{username}", "check_url": "https://mendeley.com/profiles/{username}"},
            {"name": "Kaggle", "url": "https://kaggle.com/{username}", "check_url": "https://kaggle.com/{username}"},
            {"name": "HackerRank", "url": "https://hackerrank.com/{username}", "check_url": "https://hackerrank.com/{username}"},
            {"name": "LeetCode", "url": "https://leetcode.com/{username}", "check_url": "https://leetcode.com/{username}"},
            {"name": "Codeforces", "url": "https://codeforces.com/profile/{username}", "check_url": "https://codeforces.com/profile/{username}"},
            {"name": "AtCoder", "url": "https://atcoder.jp/users/{username}", "check_url": "https://atcoder.jp/users/{username}"},
            {"name": "TopCoder", "url": "https://topcoder.com/members/{username}", "check_url": "https://topcoder.com/members/{username}"},
            {"name": "CodeChef", "url": "https://codechef.com/users/{username}", "check_url": "https://codechef.com/users/{username}"}
        ]
    
    def _respect_rate_limit(self, domain: str) -> None:
        """Rate limiting uygula"""
        with self.lock:
            current_time = time.time()
            if domain in self.rate_limits:
                time_since_last = current_time - self.rate_limits[domain]
                if time_since_last < 1.0:  # 1 saniye bekle
                    time.sleep(1.0 - time_since_last)
            self.rate_limits[domain] = current_time


def search_social_media(name: str, platform: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Sosyal medya platformlarında kişi arama
    
    Args:
        name: Aranacak kişinin adı
        platform: Belirli platform (opsiyonel)
    
    Returns:
        Bulunan profillerin listesi
    """
    engine = ProfileAnalysisEngine()
    results = []
    
    print(f"[>] Sosyal medya araması başladı: {name}")
    
    if settings.synthetic_mode:
        # Sentetik veri modu
        synthetic_profiles = [
            {
                "name": f"{name} - Twitter",
                "username": f"{name.lower().replace(' ', '_')}",
                "platform": "twitter",
                "profile_url": f"https://twitter.com/{name.lower().replace(' ', '_')}",
                "profile_picture": "https://example.com/twitter_avatar.jpg",
                "bio": f"{name} - Siber güvenlik uzmanı",
                "followers": "1.2K",
                "verified": False
            },
            {
                "name": f"{name} - LinkedIn",
                "username": f"{name.lower().replace(' ', '-')}",
                "platform": "linkedin",
                "profile_url": f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
                "profile_picture": "https://example.com/linkedin_avatar.jpg",
                "bio": f"{name} - Profesyonel profil",
                "followers": "500+",
                "verified": True
            }
        ]
        return synthetic_profiles
    
    if settings.offline_mode:
        return []
    
    try:
        # SerpAPI ile sosyal medya araması
        if settings.serpapi_key:
            search_query = f'"{name}" site:twitter.com OR site:linkedin.com OR site:instagram.com OR site:facebook.com'
            serp_results = _search_with_serpapi(search_query, engine="google", num=10)
            
            for result in serp_results:
                platform_name = _extract_platform_from_url(result.get("link", ""))
                if platform_name:
                    profile_data = {
                        "name": result.get("title", name),
                        "username": _extract_username_from_url(result.get("link", "")),
                        "platform": platform_name,
                        "profile_url": result.get("link", ""),
                        "profile_picture": "",
                        "bio": result.get("snippet", "")[:200],
                        "followers": "Bilinmiyor",
                        "verified": False
                    }
                    results.append(profile_data)
        
        # Belirli platform belirtilmişse sadece o platformu ara
        if platform:
            platform_results = _search_specific_platform(name, platform)
            results.extend(platform_results)
        
        print(f"[OK] Sosyal medya araması tamamlandı: {len(results)} profil bulundu")
        return results
        
    except Exception as e:
        print(f"[X] Sosyal medya arama hatası: {str(e)}")
        return []


def analyze_profile(profile_url: str) -> Dict[str, Any]:
    """
    Ana profil analiz motoru
    
    Args:
        profile_url: Analiz edilecek profil URL'i
    
    Returns:
        Detaylı profil analiz sonuçları
    """
    print(f"[>] Profil analizi başladı: {profile_url}")
    
    engine = ProfileAnalysisEngine()
    analysis_result = {
        "profile_url": profile_url,
        "analysis_timestamp": time.time(),
        "profile_details": {},
        "reverse_image_results": [],
        "other_accounts": [],
        "public_email": None,
        "public_photos": [],
        "risk_assessment": {},
        "ethical_warning": True
    }
    
    try:
        # 1. Profil detaylarını çek
        analysis_result["profile_details"] = fetch_profile_details(profile_url)
        
        # 2. Ters görsel arama
        if analysis_result["profile_details"].get("profile_picture"):
            analysis_result["reverse_image_results"] = reverse_image_search(
                analysis_result["profile_details"]["profile_picture"]
            )
        
        # 3. Diğer hesapları keşfet
        username = analysis_result["profile_details"].get("username")
        if username:
            analysis_result["other_accounts"] = discover_other_accounts(username)
        
        # 4. Bio'dan e-posta bul
        bio_text = analysis_result["profile_details"].get("bio", "")
        if bio_text:
            analysis_result["public_email"] = find_public_email(bio_text)
        
        # 5. Halka açık fotoğrafları listele
        analysis_result["public_photos"] = list_public_photos(profile_url)
        
        # 6. Risk değerlendirmesi
        analysis_result["risk_assessment"] = _assess_profile_risk(analysis_result)
        
        print(f"[OK] Profil analizi tamamlandı")
        return analysis_result
        
    except Exception as e:
        print(f"[X] Profil analiz hatası: {str(e)}")
        analysis_result["error"] = str(e)
        return analysis_result


def fetch_profile_details(url: str) -> Dict[str, Any]:
    """
    Profil detaylarını çek
    
    Args:
        url: Profil URL'i
    
    Returns:
        Profil detayları (username, bio, profil fotoğrafı)
    """
    engine = ProfileAnalysisEngine()
    details = {
        "username": "",
        "bio": "",
        "profile_picture": "",
        "full_name": "",
        "platform": "",
        "verification_status": False
    }
    
    try:
        domain = urlparse(url).netloc
        engine._respect_rate_limit(domain)
        
        response = engine.session.get(url, timeout=10, allow_redirects=True)
        if not response.ok:
            return details
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Platform belirleme
        if "twitter.com" in url:
            details["platform"] = "twitter"
            details.update(_parse_twitter_profile(soup, url))
        elif "linkedin.com" in url:
            details["platform"] = "linkedin"
            details.update(_parse_linkedin_profile(soup, url))
        elif "instagram.com" in url:
            details["platform"] = "instagram"
            details.update(_parse_instagram_profile(soup, url))
        elif "facebook.com" in url:
            details["platform"] = "facebook"
            details.update(_parse_facebook_profile(soup, url))
        else:
            # Genel profil parsing
            details.update(_parse_generic_profile(soup, url))
        
        # Username'i URL'den çıkar
        details["username"] = _extract_username_from_url(url)
        
        print(f"[OK] Profil detayları çekildi: {details['platform']}")
        return details
        
    except Exception as e:
        print(f"[X] Profil detay çekme hatası: {str(e)}")
        return details


def reverse_image_search(image_url: str) -> List[Dict[str, Any]]:
    """
    Ters görsel arama - SerpAPI kullanarak
    
    Args:
        image_url: Aranacak görsel URL'i
    
    Returns:
        Görselin bulunduğu web sitelerinin listesi
    """
    results = []
    
    if not settings.serpapi_key:
        print("[!] SerpAPI anahtarı bulunamadı, ters görsel arama yapılamıyor")
        return []
    
    if settings.synthetic_mode:
        # Sentetik veri
        return [
            {
                "source_url": "https://example.com/website1.com",
                "title": "Profil Fotoğrafı - Website 1",
                "image_url": image_url,
                "similarity_score": 0.95,
                "found_date": "2024-01-15"
            },
            {
                "source_url": "https://example.com/website2.com",
                "title": "Profil Fotoğrafı - Website 2", 
                "image_url": image_url,
                "similarity_score": 0.87,
                "found_date": "2024-01-10"
            }
        ]
    
    try:
        print(f"[>] Ters görsel arama başladı: {image_url}")
        
        # SerpAPI Google Images reverse search
        search_params = {
            "engine": "google_reverse_image",
            "image_url": image_url,
            "api_key": settings.serpapi_key,
            "num": 10
        }
        
        response = requests.get("https://serpapi.com/search.json", params=search_params, timeout=15)
        
        if response.ok:
            data = response.json()
            visual_matches = data.get("visual_matches", [])
            
            for match in visual_matches:
                result = {
                    "source_url": match.get("link", ""),
                    "title": match.get("title", ""),
                    "image_url": match.get("original", ""),
                    "similarity_score": match.get("similarity", 0),
                    "found_date": match.get("date", "")
                }
                results.append(result)
            
            print(f"[OK] Ters görsel arama tamamlandı: {len(results)} sonuç")
        
        time.sleep(1)  # Rate limiting
        return results
        
    except Exception as e:
        print(f"[X] Ters görsel arama hatası: {str(e)}")
        return []


def discover_other_accounts(username: str) -> List[Dict[str, Any]]:
    """
    Kullanıcı adının diğer platformlardaki varlığını kontrol et
    
    Args:
        username: Kontrol edilecek kullanıcı adı
    
    Returns:
        Bulunan hesapların listesi
    """
    engine = ProfileAnalysisEngine()
    found_accounts = []
    
    print(f"[>] Diğer hesaplar keşfediliyor: {username}")
    
    if settings.synthetic_mode:
        # Sentetik veri
        return [
            {
                "platform": "GitHub",
                "url": f"https://github.com/{username}",
                "exists": True,
                "profile_picture": "https://example.com/github_avatar.jpg",
                "bio": "Software Developer",
                "followers": "150"
            },
            {
                "platform": "Reddit", 
                "url": f"https://reddit.com/u/{username}",
                "exists": True,
                "profile_picture": "",
                "bio": "Reddit user",
                "followers": "25"
            }
        ]
    
    def check_platform(platform_info):
        """Tek platform kontrolü"""
        try:
            check_url = platform_info["check_url"].format(username=username)
            domain = urlparse(check_url).netloc
            engine._respect_rate_limit(domain)
            
            response = engine.session.head(check_url, timeout=5, allow_redirects=True)
            
            if response.status_code == 200:
                account_info = {
                    "platform": platform_info["name"],
                    "url": check_url,
                    "exists": True,
                    "profile_picture": "",
                    "bio": "",
                    "followers": ""
                }
                
                # Profil detaylarını çekmeye çalış
                try:
                    full_response = engine.session.get(check_url, timeout=8)
                    if full_response.ok:
                        soup = BeautifulSoup(full_response.content, 'html.parser')
                        # Platform-specific parsing
                        if platform_info["name"] == "GitHub":
                            account_info.update(_parse_github_profile(soup))
                        elif platform_info["name"] == "Twitter":
                            account_info.update(_parse_twitter_profile(soup, check_url))
                        # Diğer platformlar için genel parsing
                        else:
                            account_info.update(_parse_generic_profile(soup, check_url))
                except:
                    pass
                
                return account_info
            else:
                return None
                
        except Exception as e:
            print(f"[X] Platform kontrol hatası ({platform_info['name']}): {str(e)}")
            return None
    
    # Paralel platform kontrolü
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_platform = {
            executor.submit(check_platform, platform): platform 
            for platform in engine.platforms[:20]  # İlk 20 platformu kontrol et
        }
        
        for future in as_completed(future_to_platform):
            result = future.result()
            if result:
                found_accounts.append(result)
    
    print(f"[OK] Diğer hesaplar keşfedildi: {len(found_accounts)} hesap bulundu")
    return found_accounts


def find_public_email(bio_text: str) -> Optional[str]:
    """
    Bio metninden e-posta adresini bul
    
    Args:
        bio_text: Bio metni
    
    Returns:
        Bulunan e-posta adresi veya None
    """
    if not bio_text:
        return None
    
    # E-posta regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    matches = re.findall(email_pattern, bio_text)
    
    if matches:
        # İlk e-posta adresini döndür
        email = matches[0]
        print(f"[OK] Bio'da e-posta bulundu: {email}")
        return email
    
    return None


def list_public_photos(url: str) -> List[Dict[str, Any]]:
    """
    Profildeki halka açık fotoğrafları listele
    
    Args:
        url: Profil URL'i
    
    Returns:
        Fotoğraf URL'lerinin listesi
    """
    photos = []
    
    if settings.synthetic_mode:
        # Sentetik veri
        return [
            {
                "url": "https://example.com/photo1.jpg",
                "thumbnail": "https://example.com/thumb1.jpg",
                "caption": "Profil fotoğrafı",
                "date": "2024-01-15"
            },
            {
                "url": "https://example.com/photo2.jpg", 
                "thumbnail": "https://example.com/thumb2.jpg",
                "caption": "Çalışma fotoğrafı",
                "date": "2024-01-10"
            }
        ]
    
    try:
        print(f"[>] Halka açık fotoğraflar listeleniyor: {url}")
        
        engine = ProfileAnalysisEngine()
        domain = urlparse(url).netloc
        engine._respect_rate_limit(domain)
        
        response = engine.session.get(url, timeout=10)
        if not response.ok:
            return photos
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Platform-specific fotoğraf çekme
        if "instagram.com" in url:
            photos = _extract_instagram_photos(soup, url)
        elif "facebook.com" in url:
            photos = _extract_facebook_photos(soup, url)
        elif "twitter.com" in url:
            photos = _extract_twitter_photos(soup, url)
        else:
            # Genel fotoğraf çekme
            photos = _extract_generic_photos(soup, url)
        
        print(f"[OK] Halka açık fotoğraflar listelendi: {len(photos)} fotoğraf")
        return photos
        
    except Exception as e:
        print(f"[X] Fotoğraf listeleme hatası: {str(e)}")
        return photos


# Yardımcı fonksiyonlar

def _extract_platform_from_url(url: str) -> Optional[str]:
    """URL'den platform adını çıkar"""
    if "twitter.com" in url:
        return "twitter"
    elif "linkedin.com" in url:
        return "linkedin"
    elif "instagram.com" in url:
        return "instagram"
    elif "facebook.com" in url:
        return "facebook"
    elif "github.com" in url:
        return "github"
    elif "youtube.com" in url:
        return "youtube"
    return None


def _extract_username_from_url(url: str) -> str:
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
        elif "youtube.com/c/" in url:
            return url.split("youtube.com/c/")[1].split("/")[0].split("?")[0]
    except:
        pass
    return ""


def _search_with_serpapi(query: str, engine: str = "google", num: int = 10) -> List[Dict[str, Any]]:
    """SerpAPI ile arama"""
    if not settings.serpapi_key:
        return []
    
    try:
        params = {
            "engine": engine,
            "q": query,
            "api_key": settings.serpapi_key,
            "num": num
        }
        
        response = requests.get("https://serpapi.com/search.json", params=params, timeout=10)
        
        if response.ok:
            data = response.json()
            if engine == "google_images":
                return data.get("images_results", [])
            else:
                return data.get("organic_results", [])
    except Exception as e:
        print(f"[X] SerpAPI arama hatası: {str(e)}")
    
    return []


def _search_specific_platform(name: str, platform: str) -> List[Dict[str, Any]]:
    """Belirli platformda arama"""
    platform_queries = {
        "twitter": f'"{name}" site:twitter.com',
        "linkedin": f'"{name}" site:linkedin.com',
        "instagram": f'"{name}" site:instagram.com',
        "facebook": f'"{name}" site:facebook.com'
    }
    
    query = platform_queries.get(platform.lower())
    if query:
        return _search_with_serpapi(query)
    
    return []


def _assess_profile_risk(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """Profil risk değerlendirmesi"""
    risk_score = 0
    risk_factors = []
    
    # Ters görsel arama sonuçları
    if analysis_result.get("reverse_image_results"):
        risk_score += 30
        risk_factors.append("Profil fotoğrafı başka sitelerde kullanılıyor")
    
    # Çoklu hesap varlığı
    other_accounts = len(analysis_result.get("other_accounts", []))
    if other_accounts > 5:
        risk_score += 20
        risk_factors.append(f"{other_accounts} farklı platformda hesap bulundu")
    
    # Halka açık e-posta
    if analysis_result.get("public_email"):
        risk_score += 25
        risk_factors.append("Bio'da halka açık e-posta adresi bulundu")
    
    # Çok sayıda fotoğraf
    public_photos = len(analysis_result.get("public_photos", []))
    if public_photos > 10:
        risk_score += 15
        risk_factors.append(f"{public_photos} halka açık fotoğraf bulundu")
    
    # Risk seviyesi belirleme
    if risk_score >= 70:
        risk_level = "Yüksek"
    elif risk_score >= 40:
        risk_level = "Orta"
    else:
        risk_level = "Düşük"
    
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "recommendations": _generate_recommendations(risk_score, risk_factors)
    }


def _generate_recommendations(risk_score: int, risk_factors: List[str]) -> List[str]:
    """Risk bazlı öneriler oluştur"""
    recommendations = []
    
    if risk_score >= 70:
        recommendations.extend([
            "Profil fotoğrafınızı değiştirin ve eski fotoğrafları silin",
            "Halka açık bilgilerinizi gözden geçirin",
            "Gereksiz hesapları kapatın veya gizleyin",
            "E-posta adresinizi bio'dan kaldırın"
        ])
    elif risk_score >= 40:
        recommendations.extend([
            "Profil ayarlarınızı gözden geçirin",
            "Halka açık fotoğraflarınızı azaltın",
            "Güçlü gizlilik ayarları kullanın"
        ])
    else:
        recommendations.append("Mevcut gizlilik ayarlarınızı koruyun")
    
    return recommendations


# Platform-specific parsing fonksiyonları

def _parse_twitter_profile(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Twitter profil parsing"""
    details = {}
    
    try:
        # Bio
        bio_element = soup.find('div', {'data-testid': 'UserDescription'})
        if bio_element:
            details["bio"] = bio_element.get_text(strip=True)
        
        # Profil fotoğrafı
        img_element = soup.find('img', {'data-testid': 'UserAvatar'})
        if img_element:
            details["profile_picture"] = img_element.get('src', '')
        
        # Doğrulama durumu
        verified_element = soup.find('svg', {'data-testid': 'icon-verified'})
        details["verification_status"] = verified_element is not None
        
    except Exception as e:
        print(f"[X] Twitter profil parsing hatası: {str(e)}")
    
    return details


def _parse_linkedin_profile(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """LinkedIn profil parsing"""
    details = {}
    
    try:
        # Bio
        bio_element = soup.find('div', class_='text-body-medium break-words')
        if bio_element:
            details["bio"] = bio_element.get_text(strip=True)
        
        # Profil fotoğrafı
        img_element = soup.find('img', class_='pv-top-card-profile-picture__image')
        if img_element:
            details["profile_picture"] = img_element.get('src', '')
        
        # Ad
        name_element = soup.find('h1', class_='text-heading-xlarge')
        if name_element:
            details["full_name"] = name_element.get_text(strip=True)
        
    except Exception as e:
        print(f"[X] LinkedIn profil parsing hatası: {str(e)}")
    
    return details


def _parse_instagram_profile(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Instagram profil parsing"""
    details = {}
    
    try:
        # Instagram genellikle JavaScript gerektirir, bu yüzden sınırlı parsing
        bio_element = soup.find('div', class_='-vDIg')
        if bio_element:
            details["bio"] = bio_element.get_text(strip=True)
        
    except Exception as e:
        print(f"[X] Instagram profil parsing hatası: {str(e)}")
    
    return details


def _parse_facebook_profile(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Facebook profil parsing"""
    details = {}
    
    try:
        # Facebook genellikle giriş gerektirir
        bio_element = soup.find('div', {'data-testid': 'profile_tile_bio'})
        if bio_element:
            details["bio"] = bio_element.get_text(strip=True)
        
    except Exception as e:
        print(f"[X] Facebook profil parsing hatası: {str(e)}")
    
    return details


def _parse_github_profile(soup: BeautifulSoup) -> Dict[str, Any]:
    """GitHub profil parsing"""
    details = {}
    
    try:
        # Bio
        bio_element = soup.find('div', class_='p-note user-profile-bio')
        if bio_element:
            details["bio"] = bio_element.get_text(strip=True)
        
        # Profil fotoğrafı
        img_element = soup.find('img', class_='avatar avatar-user width-full border color-bg-default')
        if img_element:
            details["profile_picture"] = img_element.get('src', '')
        
    except Exception as e:
        print(f"[X] GitHub profil parsing hatası: {str(e)}")
    
    return details


def _parse_generic_profile(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Genel profil parsing"""
    details = {}
    
    try:
        # Meta description'dan bio
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            details["bio"] = meta_desc.get('content', '')
        
        # Open Graph image
        og_image = soup.find('meta', {'property': 'og:image'})
        if og_image:
            details["profile_picture"] = og_image.get('content', '')
        
        # Title'dan isim
        title = soup.find('title')
        if title:
            details["full_name"] = title.get_text(strip=True)
        
    except Exception as e:
        print(f"[X] Genel profil parsing hatası: {str(e)}")
    
    return details


def _extract_instagram_photos(soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
    """Instagram fotoğraflarını çıkar"""
    photos = []
    # Instagram genellikle JavaScript gerektirir
    return photos


def _extract_facebook_photos(soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
    """Facebook fotoğraflarını çıkar"""
    photos = []
    # Facebook genellikle giriş gerektirir
    return photos


def _extract_twitter_photos(soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
    """Twitter fotoğraflarını çıkar"""
    photos = []
    
    try:
        # Twitter medya elementlerini bul
        media_elements = soup.find_all('img', {'data-testid': 'tweetPhoto'})
        for img in media_elements:
            photo_url = img.get('src', '')
            if photo_url:
                photos.append({
                    "url": photo_url,
                    "thumbnail": photo_url,
                    "caption": "",
                    "date": ""
                })
    except Exception as e:
        print(f"[X] Twitter fotoğraf çıkarma hatası: {str(e)}")
    
    return photos


def _extract_generic_photos(soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
    """Genel fotoğraf çıkarma"""
    photos = []
    
    try:
        # Tüm img elementlerini bul
        img_elements = soup.find_all('img')
        for img in img_elements:
            src = img.get('src', '')
            if src and not src.startswith('data:'):
                # Thumbnail URL'lerini filtrele
                if any(keyword in src.lower() for keyword in ['avatar', 'profile', 'photo', 'image']):
                    photos.append({
                        "url": urljoin(url, src),
                        "thumbnail": urljoin(url, src),
                        "caption": img.get('alt', ''),
                        "date": ""
                    })
    except Exception as e:
        print(f"[X] Genel fotoğraf çıkarma hatası: {str(e)}")
    
    return photos[:10]  # Maksimum 10 fotoğraf
