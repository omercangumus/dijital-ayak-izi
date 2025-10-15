"""
Google API'leri için servis fonksiyonları
"""
import os
from typing import List, Dict, Any, Optional
from ..core.config import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
import json


def search_youtube_videos(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    YouTube'da video arama - Google YouTube Data API v3
    Endpoint: https://www.googleapis.com/youtube/v3/
    """
    if not settings.google_youtube_api_key:
        print("[!] YouTube API anahtarı bulunamadı")
        return []

    try:
        print(f"[>] YouTube arama: {query}")
        
        # YouTube Data API v3 servisini oluştur
        # Endpoint: https://www.googleapis.com/youtube/v3/
        youtube = build('youtube', 'v3', developerKey=settings.google_youtube_api_key)
        
        # Video arama
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=max_results,
            type='video'
        ).execute()
        
        results = []
        for item in search_response.get('items', []):
            video_id = item['id']['videoId']
            snippet = item['snippet']
            
            # Video detaylarını al
            video_response = youtube.videos().list(
                part='statistics,contentDetails',
                id=video_id
            ).execute()
            
            video_stats = video_response.get('items', [{}])[0].get('statistics', {})
            
            results.append({
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'video_id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'thumbnail': snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
                'channel_title': snippet.get('channelTitle', ''),
                'published_at': snippet.get('publishedAt', ''),
                'view_count': video_stats.get('viewCount', '0'),
                'like_count': video_stats.get('likeCount', '0'),
                'source': 'youtube'
            })
        
        print(f"[OK] YouTube: {len(results)} video bulundu")
        return results
        
    except HttpError as e:
        print(f"[X] YouTube API HTTP hatası: {e}")
        return []
    except Exception as e:
        print(f"[X] YouTube API genel hatası: {str(e)}")
        return []


def search_google_places(query: str, location: str = None, radius: int = 50000) -> List[Dict[str, Any]]:
    """
    Google Places API ile yer arama
    Endpoint: https://maps.googleapis.com/maps/api/place/textsearch/json
    """
    if not settings.google_places_api_key:
        print("[!] Places API anahtarı bulunamadı")
        return []

    try:
        print(f"[>] Google Places arama: {query}")
        
        # Places API endpoint - Doğrulanmış endpoint
        # https://maps.googleapis.com/maps/api/place/textsearch/json
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        
        params = {
            'query': query,
            'key': settings.google_places_api_key,
            'language': 'tr'
        }
        
        if location:
            params['location'] = location
            params['radius'] = radius
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('status') != 'OK':
            print(f"[X] Places API hatası: {data.get('status')}")
            return []
        
        results = []
        for place in data.get('results', []):
            results.append({
                'name': place.get('name', ''),
                'address': place.get('formatted_address', ''),
                'place_id': place.get('place_id', ''),
                'rating': place.get('rating', 0),
                'price_level': place.get('price_level', 0),
                'types': place.get('types', []),
                'geometry': place.get('geometry', {}),
                'photos': place.get('photos', []),
                'source': 'google_places'
            })
        
        print(f"[OK] Google Places: {len(results)} yer bulundu")
        return results
        
    except Exception as e:
        print(f"[X] Google Places API hatası: {str(e)}")
        return []


def analyze_image_with_vision(image_url: str) -> Dict[str, Any]:
    """
    Google Vision API ile görsel analiz
    Endpoint: https://vision.googleapis.com/v1/images:annotate
    """
    if not settings.google_vision_api_key:
        print("[!] Vision API anahtarı bulunamadı")
        return {}

    try:
        print(f"[>] Vision API görsel analizi: {image_url}")
        
        # Vision API endpoint - Doğrulanmış endpoint
        # https://vision.googleapis.com/v1/images:annotate
        url = f"https://vision.googleapis.com/v1/images:annotate?key={settings.google_vision_api_key}"
        
        payload = {
            "requests": [
                {
                    "image": {
                        "source": {
                            "imageUri": image_url
                        }
                    },
                    "features": [
                        {"type": "LABEL_DETECTION", "maxResults": 10},
                        {"type": "FACE_DETECTION", "maxResults": 10},
                        {"type": "TEXT_DETECTION", "maxResults": 10},
                        {"type": "OBJECT_LOCALIZATION", "maxResults": 10},
                        {"type": "LANDMARK_DETECTION", "maxResults": 10}
                    ]
                }
            ]
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if 'responses' not in data or not data['responses']:
            print("[X] Vision API yanıt hatası")
            return {}
        
        result = data['responses'][0]
        
        analysis = {
            'labels': [],
            'faces': [],
            'text': [],
            'objects': [],
            'landmarks': []
        }
        
        # Etiketler
        if 'labelAnnotations' in result:
            for label in result['labelAnnotations']:
                analysis['labels'].append({
                    'description': label.get('description', ''),
                    'score': label.get('score', 0)
                })
        
        # Yüzler
        if 'faceAnnotations' in result:
            for face in result['faceAnnotations']:
                analysis['faces'].append({
                    'joy_likelihood': face.get('joyLikelihood', 'UNKNOWN'),
                    'sorrow_likelihood': face.get('sorrowLikelihood', 'UNKNOWN'),
                    'anger_likelihood': face.get('angerLikelihood', 'UNKNOWN'),
                    'surprise_likelihood': face.get('surpriseLikelihood', 'UNKNOWN')
                })
        
        # Metin
        if 'textAnnotations' in result:
            for text in result['textAnnotations']:
                analysis['text'].append({
                    'description': text.get('description', ''),
                    'bounding_poly': text.get('boundingPoly', {})
                })
        
        # Nesneler
        if 'localizedObjectAnnotations' in result:
            for obj in result['localizedObjectAnnotations']:
                analysis['objects'].append({
                    'name': obj.get('name', ''),
                    'score': obj.get('score', 0)
                })
        
        # Yer işaretleri
        if 'landmarkAnnotations' in result:
            for landmark in result['landmarkAnnotations']:
                analysis['landmarks'].append({
                    'description': landmark.get('description', ''),
                    'score': landmark.get('score', 0)
                })
        
        print(f"[OK] Vision API analizi tamamlandı")
        return analysis
        
    except Exception as e:
        print(f"[X] Vision API hatası: {str(e)}")
        return {}


def get_geolocation_info(address: str) -> Dict[str, Any]:
    """
    Google Maps Geocoding API ile adres bilgisi
    Endpoint: https://maps.googleapis.com/maps/api/geocode/json
    """
    if not settings.google_maps_api_key:
        print("[!] Maps API anahtarı bulunamadı")
        return {}

    try:
        print(f"[>] Geocoding API: {address}")
        
        # Geocoding API endpoint - Doğrulanmış endpoint
        # https://maps.googleapis.com/maps/api/geocode/json
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        
        params = {
            'address': address,
            'key': settings.google_maps_api_key,
            'language': 'tr'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('status') != 'OK':
            print(f"[X] Geocoding API hatası: {data.get('status')}")
            return {}
        
        if not data.get('results'):
            return {}
        
        result = data['results'][0]
        geometry = result.get('geometry', {})
        location = geometry.get('location', {})
        
        geolocation_info = {
            'formatted_address': result.get('formatted_address', ''),
            'latitude': location.get('lat', 0),
            'longitude': location.get('lng', 0),
            'place_id': result.get('place_id', ''),
            'types': result.get('types', []),
            'address_components': result.get('address_components', [])
        }
        
        print(f"[OK] Geocoding API tamamlandı")
        return geolocation_info
        
    except Exception as e:
        print(f"[X] Geocoding API hatası: {str(e)}")
        return {}
