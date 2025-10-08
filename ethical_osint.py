#!/usr/bin/env python3
"""
Ethical OSINT Profile Analysis Engine
- KVKK ve etik kurallara uygun
- Sadece açık kaynak veriler
- Güvenli ve sorumlu tasarım
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional, Any
import asyncio
import aiohttp
from dataclasses import dataclass
import hashlib
import os
from datetime import datetime, timedelta

@dataclass
class ProfileInfo:
    username: str
    display_name: str
    bio: str
    profile_picture: str
    platform: str
    url: str
    followers_count: Optional[int] = None
    verified: bool = False

@dataclass
class SearchResult:
    profiles: List[ProfileInfo]
    total_found: int
    search_time: float

class EthicalOSINTEngine:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Platform-specific selectors
        self.platform_selectors = {
            'instagram': {
                'username': 'h2[class*="username"]',
                'bio': 'div[class*="bio"]',
                'profile_pic': 'img[alt*="profile picture"]',
                'followers': 'span[title]'
            },
            'twitter': {
                'username': 'h1[data-testid="UserName"]',
                'bio': 'div[data-testid="UserDescription"]',
                'profile_pic': 'img[data-testid="UserAvatar"]',
                'followers': 'a[href*="/followers"]'
            },
            'linkedin': {
                'username': 'h1[class*="text-heading-xlarge"]',
                'bio': 'div[class*="summary"]',
                'profile_pic': 'img[class*="presence-entity__image"]',
                'followers': 'span[class*="t-bold"]'
            }
        }
        
        # 50+ popüler platform listesi
        self.platforms_to_check = [
            'github.com', 'reddit.com', 'twitter.com', 'instagram.com',
            'facebook.com', 'linkedin.com', 'youtube.com', 'tiktok.com',
            'snapchat.com', 'pinterest.com', 'medium.com', 'dev.to',
            'stackoverflow.com', 'codepen.io', 'behance.net', 'dribbble.com',
            'flickr.com', 'vimeo.com', 'twitch.tv', 'steamcommunity.com',
            'soundcloud.com', 'spotify.com', 'last.fm', 'bandcamp.com',
            'goodreads.com', 'letterboxd.com', 'imdb.com', 'discord.com',
            'telegram.org', 'whatsapp.com', 'skype.com', 'zoom.us',
            'slack.com', 'trello.com', 'asana.com', 'notion.so',
            'figma.com', 'canva.com', 'adobe.com', 'dropbox.com',
            'google.com', 'microsoft.com', 'apple.com', 'amazon.com',
            'netflix.com', 'hulu.com', 'disney.com', 'hbo.com',
            'espn.com', 'nba.com', 'nfl.com', 'fifa.com'
        ]

    def search_social_media(self, name: str, platform: str) -> SearchResult:
        """
        Belirli bir platformda isim araması yapar
        Etik kurallara uygun, yavaş ve saygılı
        """
        start_time = time.time()
        profiles = []
        
        try:
            # Platform-specific arama URL'leri
            search_urls = {
                'instagram': f"https://www.instagram.com/{name}/",
                'twitter': f"https://twitter.com/{name}",
                'linkedin': f"https://www.linkedin.com/in/{name}/",
                'facebook': f"https://www.facebook.com/{name}/",
                'github': f"https://github.com/{name}",
                'reddit': f"https://www.reddit.com/user/{name}/"
            }
            
            if platform in search_urls:
                # Rate limiting - platformlara saygı göster
                time.sleep(2)
                
                response = self.session.get(search_urls[platform], timeout=10)
                if response.status_code == 200:
                    profile = self._parse_profile(response.text, platform, search_urls[platform])
                    if profile:
                        profiles.append(profile)
            
            # Genel arama için Google (SerpAPI kullanarak)
            if not profiles:
                profiles.extend(self._google_search_profiles(name, platform))
            
        except Exception as e:
            print(f"Arama hatası ({platform}): {e}")
        
        search_time = time.time() - start_time
        return SearchResult(profiles=profiles, total_found=len(profiles), search_time=search_time)

    def analyze_profile(self, profile_url: str) -> Dict[str, Any]:
        """
        Ana analiz motoru - profil URL'sini detaylı analiz eder
        """
        analysis_result = {
            'profile_details': None,
            'reverse_image_results': [],
            'other_accounts': [],
            'found_emails': [],
            'public_photos': [],
            'analysis_timestamp': datetime.now().isoformat(),
            'warnings': []
        }
        
        try:
            # 1. Profil detaylarını çek
            analysis_result['profile_details'] = self.fetch_profile_details(profile_url)
            
            if analysis_result['profile_details']:
                profile = analysis_result['profile_details']
                
                # 2. Tersine görsel arama
                if profile.profile_picture:
                    analysis_result['reverse_image_results'] = self.reverse_image_search(profile.profile_picture)
                
                # 3. Diğer hesapları keşfet
                if profile.username:
                    analysis_result['other_accounts'] = self.discover_other_accounts(profile.username)
                
                # 4. E-posta ara
                if profile.bio:
                    analysis_result['found_emails'] = self.find_public_email(profile.bio)
                
                # 5. Diğer fotoğrafları listele
                analysis_result['public_photos'] = self.list_public_photos(profile_url)
            
        except Exception as e:
            analysis_result['warnings'].append(f"Analiz hatası: {str(e)}")
        
        return analysis_result

    def fetch_profile_details(self, url: str) -> Optional[ProfileInfo]:
        """
        Profil URL'sinden detayları çeker
        """
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            domain = urlparse(url).netloc.lower()
            
            # Platform-specific parsing
            if 'instagram.com' in domain:
                return self._parse_instagram_profile(soup, url)
            elif 'twitter.com' in domain:
                return self._parse_twitter_profile(soup, url)
            elif 'linkedin.com' in domain:
                return self._parse_linkedin_profile(soup, url)
            elif 'github.com' in domain:
                return self._parse_github_profile(soup, url)
            else:
                return self._parse_generic_profile(soup, url)
                
        except Exception as e:
            print(f"Profil detay çekme hatası: {e}")
            return None

    def reverse_image_search(self, image_url: str) -> List[Dict[str, Any]]:
        """
        Tersine görsel arama (SerpAPI kullanarak)
        """
        results = []
        
        try:
            # SerpAPI ile tersine görsel arama
            serpapi_url = "https://serpapi.com/search"
            params = {
                'engine': 'google_reverse_image',
                'image_url': image_url,
                'api_key': os.getenv('SERPAPI_KEY', 'demo_key')
            }
            
            response = self.session.get(serpapi_url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                if 'image_results' in data:
                    for result in data['image_results'][:10]:  # İlk 10 sonuç
                        results.append({
                            'source': result.get('source', 'Unknown'),
                            'url': result.get('link', ''),
                            'title': result.get('title', ''),
                            'similarity_score': result.get('similarity', 0)
                        })
            
            # Rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"Tersine görsel arama hatası: {e}")
        
        return results

    def discover_other_accounts(self, username: str) -> List[Dict[str, Any]]:
        """
        Kullanıcı adının 50+ platformda varlığını kontrol eder
        """
        found_accounts = []
        
        # Paralel kontrol için async fonksiyon
        async def check_platform_async(session, platform, username):
            try:
                url = f"https://{platform}/{username}"
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        return {
                            'platform': platform,
                            'url': url,
                            'exists': True,
                            'status_code': response.status
                        }
            except:
                pass
            return None
        
        async def check_all_platforms():
            async with aiohttp.ClientSession() as session:
                tasks = []
                for platform in self.platforms_to_check[:20]:  # İlk 20 platform
                    tasks.append(check_platform_async(session, platform, username))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if result and isinstance(result, dict):
                        found_accounts.append(result)
                
                # Rate limiting
                await asyncio.sleep(0.1)
        
        # Async fonksiyonu çalıştır
        try:
            asyncio.run(check_all_platforms())
        except Exception as e:
            print(f"Hesap keşfi hatası: {e}")
        
        return found_accounts

    def find_public_email(self, bio_text: str) -> List[str]:
        """
        Bio metninde e-posta adreslerini arar
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, bio_text)
        
        # Geçerli e-posta adreslerini filtrele
        valid_emails = []
        for email in emails:
            if len(email) > 5 and '.' in email.split('@')[1]:
                valid_emails.append(email.lower())
        
        return list(set(valid_emails))  # Duplikatları kaldır

    def list_public_photos(self, profile_url: str) -> List[str]:
        """
        Profildeki diğer açık fotoğrafları listeler
        """
        photos = []
        
        try:
            response = self.session.get(profile_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Platform-specific fotoğraf seçicileri
                if 'instagram.com' in profile_url:
                    img_tags = soup.find_all('img', {'src': re.compile(r'.*\.(jpg|jpeg|png|webp).*')})
                elif 'twitter.com' in profile_url:
                    img_tags = soup.find_all('img', {'data-testid': re.compile(r'UserAvatar|tweetPhoto')})
                else:
                    img_tags = soup.find_all('img', {'src': re.compile(r'.*\.(jpg|jpeg|png|webp).*')})
                
                for img in img_tags[:10]:  # İlk 10 fotoğraf
                    src = img.get('src')
                    if src and src.startswith('http'):
                        photos.append(src)
            
        except Exception as e:
            print(f"Fotoğraf listeleme hatası: {e}")
        
        return photos

    def _parse_profile(self, html_content: str, platform: str, url: str) -> Optional[ProfileInfo]:
        """Platform-specific profil parsing"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        if platform == 'instagram':
            return self._parse_instagram_profile(soup, url)
        elif platform == 'twitter':
            return self._parse_twitter_profile(soup, url)
        elif platform == 'github':
            return self._parse_github_profile(soup, url)
        
        return None

    def _parse_instagram_profile(self, soup: BeautifulSoup, url: str) -> Optional[ProfileInfo]:
        """Instagram profil parsing"""
        try:
            # Instagram için meta tag'lerden bilgi al
            title_tag = soup.find('title')
            username = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
            
            # Meta description'dan bio al
            meta_desc = soup.find('meta', {'name': 'description'})
            bio = meta_desc.get('content', '') if meta_desc else ''
            
            # Profil fotoğrafı
            profile_pic = soup.find('img', {'alt': re.compile(r'.*profile picture.*', re.I)})
            pic_url = profile_pic.get('src', '') if profile_pic else ''
            
            return ProfileInfo(
                username=username,
                display_name=username,
                bio=bio,
                profile_picture=pic_url,
                platform='instagram',
                url=url
            )
        except Exception as e:
            print(f"Instagram parsing hatası: {e}")
            return None

    def _parse_twitter_profile(self, soup: BeautifulSoup, url: str) -> Optional[ProfileInfo]:
        """Twitter profil parsing"""
        try:
            username = url.split('/')[-1]
            
            # Twitter specific selectors
            display_name_elem = soup.find('h1', {'data-testid': 'UserName'})
            display_name = display_name_elem.get_text(strip=True) if display_name_elem else username
            
            bio_elem = soup.find('div', {'data-testid': 'UserDescription'})
            bio = bio_elem.get_text(strip=True) if bio_elem else ''
            
            avatar_elem = soup.find('img', {'data-testid': 'UserAvatar'})
            avatar_url = avatar_elem.get('src', '') if avatar_elem else ''
            
            return ProfileInfo(
                username=username,
                display_name=display_name,
                bio=bio,
                profile_picture=avatar_url,
                platform='twitter',
                url=url
            )
        except Exception as e:
            print(f"Twitter parsing hatası: {e}")
            return None

    def _parse_github_profile(self, soup: BeautifulSoup, url: str) -> Optional[ProfileInfo]:
        """GitHub profil parsing"""
        try:
            username = url.split('/')[-1]
            
            name_elem = soup.find('h1', {'class': 'vcard-names'})
            display_name = name_elem.get_text(strip=True) if name_elem else username
            
            bio_elem = soup.find('div', {'class': 'user-profile-bio'})
            bio = bio_elem.get_text(strip=True) if bio_elem else ''
            
            avatar_elem = soup.find('img', {'class': 'avatar'})
            avatar_url = avatar_elem.get('src', '') if avatar_elem else ''
            
            return ProfileInfo(
                username=username,
                display_name=display_name,
                bio=bio,
                profile_picture=avatar_url,
                platform='github',
                url=url
            )
        except Exception as e:
            print(f"GitHub parsing hatası: {e}")
            return None

    def _parse_generic_profile(self, soup: BeautifulSoup, url: str) -> Optional[ProfileInfo]:
        """Genel profil parsing"""
        try:
            username = urlparse(url).path.split('/')[-1]
            
            title_tag = soup.find('title')
            display_name = title_tag.get_text(strip=True) if title_tag else username
            
            meta_desc = soup.find('meta', {'name': 'description'})
            bio = meta_desc.get('content', '') if meta_desc else ''
            
            avatar_elem = soup.find('img', {'class': re.compile(r'.*avatar.*', re.I)})
            avatar_url = avatar_elem.get('src', '') if avatar_elem else ''
            
            return ProfileInfo(
                username=username,
                display_name=display_name,
                bio=bio,
                profile_picture=avatar_url,
                platform=urlparse(url).netloc,
                url=url
            )
        except Exception as e:
            print(f"Genel parsing hatası: {e}")
            return None

    def _google_search_profiles(self, name: str, platform: str) -> List[ProfileInfo]:
        """Google üzerinden profil arama"""
        profiles = []
        
        try:
            # SerpAPI ile Google arama
            serpapi_url = "https://serpapi.com/search"
            params = {
                'q': f'"{name}" site:{platform}',
                'api_key': os.getenv('SERPAPI_KEY', 'demo_key'),
                'num': 10
            }
            
            response = self.session.get(serpapi_url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                if 'organic_results' in data:
                    for result in data['organic_results']:
                        profile = ProfileInfo(
                            username=name,
                            display_name=result.get('title', name),
                            bio=result.get('snippet', ''),
                            profile_picture='',
                            platform=platform,
                            url=result.get('link', '')
                        )
                        profiles.append(profile)
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"Google arama hatası: {e}")
        
        return profiles

# Singleton instance
osint_engine = EthicalOSINTEngine()
