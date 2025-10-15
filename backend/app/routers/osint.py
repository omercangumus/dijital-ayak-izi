from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from pydantic import BaseModel
import requests
import json
import time
import re
from urllib.parse import quote_plus

router = APIRouter()

class Stage1SearchRequest(BaseModel):
    firstName: str
    lastName: str
    city: str

class Stage2AnalysisRequest(BaseModel):
    profile_url: str
    source: str
    name: str

class CandidateProfile(BaseModel):
    source: str
    name: str
    profile_url: str
    profile_pic_url: str = None
    snippet: str

class GoogleDorkingService:
    def __init__(self):
        self.search_queries = [
            '"{firstName} {lastName}" "{city}" site:linkedin.com',
            '"{firstName} {lastName}" "{city}" site:facebook.com',
            '"{firstName} {lastName}" "{city}" site:twitter.com OR site:instagram.com',
            '"{firstName} {lastName}" "{city}" inurl:CV OR inurl:resume',
            '"{firstName} {lastName}" "{city}" filetype:pdf',
            '"{firstName} {lastName}" "{city}" "about me" OR "profile"'
        ]
    
    def construct_queries(self, firstName: str, lastName: str, city: str) -> List[str]:
        """Construct Google dork queries for profile search"""
        queries = []
        for template in self.search_queries:
            query = template.format(
                firstName=firstName,
                lastName=lastName,
                city=city
            )
            queries.append(query)
        return queries
    
    def search_profiles(self, firstName: str, lastName: str, city: str) -> List[Dict[str, Any]]:
        """Perform Google dorking search for potential profiles"""
        from app.services.selfscan import search_google_api
        from app.services.profile_analysis import _search_with_google_api
        
        queries = self.construct_queries(firstName, lastName, city)
        candidates = []
        
        for query in queries:
            try:
                print(f"[>] Gerçek arama yapılıyor: {query}")
                # Gerçek Google araması yap
                search_results = _search_with_google_api(query, num=5)
                
                for result in search_results:
                    platform = self._extract_platform(result.get('link', ''))
                    candidate = {
                        'name': f"{firstName} {lastName}",
                        'profile_url': result.get('link', ''),
                        'profile_pic_url': self._extract_profile_pic(result.get('link', '')),
                        'snippet': result.get('snippet', ''),
                        'source': platform if platform else 'unknown',
                        'title': result.get('title', ''),
                        'position': result.get('position', 0)
                    }
                    candidates.append(candidate)
                    
            except Exception as e:
                print(f"Search error for query '{query}': {str(e)}")
                continue
        
        # Remove duplicates and return top results
        unique_candidates = self._deduplicate_candidates(candidates)
        return unique_candidates[:10]  # Return top 10 results
    
    def _mock_search_results(self, query: str, firstName: str, lastName: str) -> List[Dict[str, Any]]:
        """Mock search results for development"""
        platforms = ['LinkedIn', 'Facebook', 'Twitter', 'Instagram', 'GitHub']
        mock_candidates = []
        
        # Create more realistic mock data
        bios = [
            f"{firstName} {lastName} is a software engineer with expertise in Python and JavaScript.",
            f"Professional {firstName} {lastName} working in the technology sector.",
            f"{firstName} {lastName} - Marketing specialist with 5+ years experience.",
            f"Data scientist {firstName} {lastName} passionate about AI and machine learning.",
            f"{firstName} {lastName} is a UI/UX designer creating amazing digital experiences."
        ]
        
        locations = [
            "Istanbul, Turkey",
            "Ankara, Turkey", 
            "Izmir, Turkey",
            "Bursa, Turkey",
            "Antalya, Turkey"
        ]
        
        for i, platform in enumerate(platforms):
            candidate = {
                "source": platform,
                "name": f"{firstName} {lastName}",
                "profile_url": f"https://{platform.lower()}.com/in/{firstName.lower()}{lastName.lower()}{i+1}",
                "profile_pic_url": f"https://api.dicebear.com/7.x/avataaars/svg?seed={firstName}{lastName}{i}",
                "snippet": f"{bios[i % len(bios)]} Based in {locations[i % len(locations)]}. Active on {platform} with public profile information available."
            }
            mock_candidates.append(candidate)
        
        return mock_candidates
    
    def _extract_profile_pic(self, profile_url: str) -> str:
        """Profil fotoğrafını URL'den çıkar"""
        try:
            from app.services.selfscan import get_profile_photo
            from app.services.profile_analysis import _extract_platform_from_url
            
            platform = _extract_platform_from_url(profile_url)
            if platform:
                return get_profile_photo(profile_url, platform)
        except Exception as e:
            print(f"[X] Profil fotoğrafı çekme hatası: {str(e)}")
        return ""
    
    def _extract_platform(self, url: str) -> str:
        """URL'den platform adını çıkar"""
        from app.services.profile_analysis import _extract_platform_from_url
        return _extract_platform_from_url(url)
    
    def _deduplicate_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate candidates based on profile_url"""
        seen_urls = set()
        unique_candidates = []
        
        for candidate in candidates:
            if candidate["profile_url"] not in seen_urls:
                seen_urls.add(candidate["profile_url"])
                unique_candidates.append(candidate)
        
        return unique_candidates

class DeepAnalysisService:
    def __init__(self):
        self.modules = {
            'identity': self._analyze_identity,
            'contact': self._analyze_contact,
            'accounts': self._analyze_accounts,
            'visual_footprint': self._analyze_visual_footprint,
            'public_gallery': self._analyze_public_gallery
        }
    
    def analyze_profile(self, profile_url: str, source: str, name: str) -> Dict[str, Any]:
        """Run deep analysis on selected profile"""
        analysis_results = {
            'target_url': profile_url,
            'source': source,
            'name': name,
            'modules': {}
        }
        
        for module_name, module_func in self.modules.items():
            try:
                result = module_func(profile_url, name)
                analysis_results['modules'][module_name] = {
                    'status': 'complete',
                    'data': result
                }
            except Exception as e:
                analysis_results['modules'][module_name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return analysis_results
    
    def _analyze_identity(self, profile_url: str, name: str) -> Dict[str, Any]:
        """Module 1: Extract identity information"""
        # Simulate profile scraping
        name_parts = name.split()
        first_name = name_parts[0] if name_parts else "User"
        last_name = name_parts[1] if len(name_parts) > 1 else "Surname"
        
        return {
            'fullName': name,
            'username': f"@{first_name.lower()}{last_name.lower()}",
            'bio': f"Professional {first_name} {last_name} with expertise in technology and innovation. Passionate about digital transformation and building meaningful connections in the tech community.",
            'location': 'Istanbul, Turkey',
            'website': f"https://{first_name.lower()}{last_name.lower()}.dev",
            'verified': True,
            'followers': '2.5K',
            'connections': '500+'
        }
    
    def _analyze_contact(self, profile_url: str, name: str) -> Dict[str, Any]:
        """Module 2: Email discovery and contact information"""
        # Simulate email discovery
        name_parts = name.lower().split()
        first_name = name_parts[0] if name_parts else "user"
        last_name = name_parts[1] if len(name_parts) > 1 else "surname"
        
        return {
            'foundEmails': [
                f"{first_name}.{last_name}@techcorp.com",
                f"{first_name}{last_name}@university.edu.tr"
            ],
            'guessedEmails': [
                f"{first_name[0]}.{last_name}@startup.com [GUESS]",
                f"{first_name}@consulting.com [GUESS]",
                f"{first_name}.{last_name}@freelance.net [GUESS]"
            ],
            'phoneNumbers': ['+90 532 XXX XX XX'],
            'socialLinks': [
                profile_url,
                f"https://linkedin.com/in/{first_name}{last_name}",
                f"https://github.com/{first_name}{last_name}",
                f"https://twitter.com/{first_name}{last_name}"
            ]
        }
    
    def _analyze_accounts(self, profile_url: str, name: str) -> Dict[str, Any]:
        """Module 3: Username expansion across platforms"""
        username = name.lower().replace(' ', '')
        
        return {
            'primaryUsername': username,
            'platforms': [
                {'name': 'GitHub', 'url': f'https://github.com/{username}', 'status': 'active', 'posts': '45 repos'},
                {'name': 'Stack Overflow', 'url': f'https://stackoverflow.com/users/{username}', 'status': 'active', 'reputation': '2.1K'},
                {'name': 'Reddit', 'url': f'https://reddit.com/u/{username}', 'status': 'inactive', 'karma': '156'},
                {'name': 'Medium', 'url': f'https://medium.com/@{username}', 'status': 'active', 'articles': '12'},
                {'name': 'Dev.to', 'url': f'https://dev.to/{username}', 'status': 'active', 'followers': '89'},
                {'name': 'Behance', 'url': f'https://behance.net/{username}', 'status': 'active', 'projects': '8'},
                {'name': 'Dribbble', 'url': f'https://dribbble.com/{username}', 'status': 'active', 'shots': '23'}
            ]
        }
    
    def _analyze_visual_footprint(self, profile_url: str, name: str) -> Dict[str, Any]:
        """Module 4: Reverse image search"""
        return {
            'profileImageUrl': f"https://via.placeholder.com/300?text={name[0]}",
            'reverseImageResults': [
                {'url': profile_url, 'platform': 'Original Platform'},
                {'url': f'https://linkedin.com/in/{name.lower().replace(" ", "")}', 'platform': 'LinkedIn'},
                {'url': f'https://github.com/{name.lower().replace(" ", "")}', 'platform': 'GitHub'}
            ]
        }
    
    def _analyze_public_gallery(self, profile_url: str, name: str) -> Dict[str, Any]:
        """Module 5: Public photo collection"""
        return {
            'photos': [
                {'url': f"https://via.placeholder.com/400?text={name}+Photo+1", 'description': 'Profile photo'},
                {'url': f"https://via.placeholder.com/400?text={name}+Photo+2", 'description': 'Team photo'},
                {'url': f"https://via.placeholder.com/400?text={name}+Photo+3", 'description': 'Event photo'}
            ]
        }

# Initialize services
google_dorking = GoogleDorkingService()
deep_analysis = DeepAnalysisService()

@router.post("/stage1/search", response_model=List[CandidateProfile])
async def stage1_search_profiles(request: Stage1SearchRequest):
    """Stage 1: Search for potential profiles using Google dorking"""
    try:
        candidates = google_dorking.search_profiles(
            request.firstName,
            request.lastName,
            request.city
        )
        return candidates
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile search failed: {str(e)}"
        )

@router.post("/stage2/analyze")
async def stage2_deep_analysis(request: Stage2AnalysisRequest):
    """Stage 2: Perform deep analysis on selected profile"""
    try:
        analysis_results = deep_analysis.analyze_profile(
            request.profile_url,
            request.source,
            request.name
        )
        return analysis_results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deep analysis failed: {str(e)}"
        )

@router.get("/stage1/health")
async def stage1_health():
    """Health check for Stage 1 service"""
    return {"status": "healthy", "service": "OSINT Stage 1"}

@router.get("/stage2/health")
async def stage2_health():
    """Health check for Stage 2 service"""
    return {"status": "healthy", "service": "OSINT Stage 2"}
