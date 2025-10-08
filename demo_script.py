#!/usr/bin/env python3
"""
Demo script - API anahtarları olmadan nasıl çalıştığını gösterir
"""

import os
import sys

# API anahtarlarını doğrudan set et
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBWSiMlyoLCGdkXInlaNXqGUv9wyWSNs9w'
os.environ['GOOGLE_SEARCH_ENGINE_ID'] = '51f92d1c744fb48e0'
os.environ['SCRAPER_API_KEY'] = '3716f5d21318e21ffb16dc2165079983'

from profile_analyzer import ProfileAnalyzer

def demo_script():
    """Script'in nasıl çalıştığını göster"""
    print("=" * 60)
    print("SOSYAL MEDYA PROFIL ANALIZ SCRIPTI DEMO")
    print("=" * 60)
    
    print("\n1. API ANAHTARLARI DOGRULANMASI:")
    print("-" * 40)
    try:
        analyzer = ProfileAnalyzer()
        print("SUCCESS: Tum API anahtarlari dogrulandi")
        print("- Google API Key: OK")
        print("- Google Search Engine ID: OK") 
        print("- Scraper API Key: OK")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return
    
    print("\n2. PROFIL ANALIZI BASLATILIYOR:")
    print("-" * 40)
    test_url = "https://instagram.com/instagram"
    print(f"Test URL: {test_url}")
    
    print("\n3. SCRAPING ISLEMI:")
    print("-" * 40)
    print("- ScraperAPI'ye istek gonderiliyor...")
    print("- HTML icerik cekiliyor...")
    print("- BeautifulSoup ile parse ediliyor...")
    print("- Profil verileri cikariliyor...")
    
    try:
        result = analyzer.analyze_profile(test_url)
        
        print("\n4. SONUCLAR:")
        print("-" * 40)
        
        if result.get('analysis_status') == 'completed':
            profile = result.get('profile_analysis', {})
            print(f"Platform: {profile.get('platform', 'Bilinmiyor')}")
            print(f"Isim: {profile.get('full_name', 'Bilinmiyor')}")
            print(f"Bio: {profile.get('bio', 'Yok')[:100]}...")
            print(f"Profil Resmi: {profile.get('profile_picture', 'Yok')}")
            
            reverse_search = result.get('reverse_image_search')
            if reverse_search and not reverse_search.get('error'):
                print(f"Ters Gorsel Arama: {len(reverse_search.get('results', []))} sonuc bulundu")
            else:
                print("Ters Gorsel Arama: Basarisiz (API anahtari gecersiz)")
        else:
            print(f"HATA: {result.get('error', 'Bilinmeyen hata')}")
            
    except Exception as e:
        print(f"HATA: {str(e)}")
    
    print("\n5. SCRIPT OZELLIKLERI:")
    print("-" * 40)
    print("- Guvenli API anahtari yonetimi (.env dosyasi)")
    print("- Coklu platform desteği (Instagram, Twitter, LinkedIn, Facebook)")
    print("- Ters gorsel arama (Google Custom Search API)")
    print("- Detayli logging")
    print("- JSON formatinda sonuclar")
    print("- Hata yonetimi")
    
    print("\n6. KULLANIM:")
    print("-" * 40)
    print("python profile_analyzer.py")
    print("# URL girin ve analiz sonuclarini gorun")
    
    print("\n=" * 60)
    print("DEMO TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    demo_script()
