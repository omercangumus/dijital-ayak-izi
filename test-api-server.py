#!/usr/bin/env python3
"""
API Server Test Script

Bu script, çalışan API server'ını test eder ve örnek analizler yapar.
"""

import requests
import json
import time
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:5001"

def test_health():
    """Health check test"""
    print("🏥 Health Check Test...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"   Analyzer Ready: {data['analyzer_ready']}")
            return True
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {str(e)}")
        return False

def test_root():
    """Root endpoint test"""
    print("\n🌐 Root Endpoint Test...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root Endpoint: {data['message']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ Root Endpoint Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root Endpoint Error: {str(e)}")
        return False

def test_analyze(profile_url: str) -> Dict[str, Any]:
    """Analyze endpoint test"""
    print(f"\n🔍 Analyze Test: {profile_url}")
    
    payload = {
        "profile_url": profile_url
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=payload,
            timeout=60
        )
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success']:
                print(f"✅ Analysis Successful!")
                print(f"   Processing Time: {data['processing_time']}s")
                
                profile = data['data']['profile_analysis']
                print(f"   Platform: {profile['platform']}")
                print(f"   Name: {profile.get('full_name', 'N/A')}")
                print(f"   Bio: {profile.get('bio', 'N/A')[:100]}...")
                
                reverse_search = data['data']['reverse_image_search']
                if reverse_search and not reverse_search.get('error'):
                    print(f"   Reverse Image Results: {len(reverse_search['results'])}")
                
                return data
            else:
                print(f"❌ Analysis Failed: {data['error']}")
                return data
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Request Timeout!")
        return None
    except Exception as e:
        print(f"❌ Analysis Error: {str(e)}")
        return None

def test_invalid_request():
    """Invalid request test"""
    print("\n🚫 Invalid Request Test...")
    
    # Geçersiz URL
    payload = {
        "profile_url": "not-a-valid-url"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 422:  # Validation Error
            print("✅ Invalid Request Correctly Rejected")
            return True
        else:
            print(f"❌ Expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Invalid Request Test Error: {str(e)}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🧪 API Server Test Suite")
    print("=" * 50)
    
    # Test sırası
    tests_passed = 0
    total_tests = 0
    
    # 1. Health Check
    total_tests += 1
    if test_health():
        tests_passed += 1
    
    # 2. Root Endpoint
    total_tests += 1
    if test_root():
        tests_passed += 1
    
    # 3. Invalid Request
    total_tests += 1
    if test_invalid_request():
        tests_passed += 1
    
    # 4. Analyze Tests
    test_urls = [
        "https://www.instagram.com/nasa/",
        "https://twitter.com/elonmusk",
        "https://www.linkedin.com/in/satyanadella/"
    ]
    
    for url in test_urls:
        total_tests += 1
        result = test_analyze(url)
        if result and result.get('success'):
            tests_passed += 1
            break  # Bir tane başarılı olması yeterli
    
    # Sonuçları göster
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed!")
    elif tests_passed > 0:
        print("⚠️  Some tests passed")
    else:
        print("❌ All tests failed!")
    
    print("\n💡 Tips:")
    print("   - API Docs: http://localhost:5001/docs")
    print("   - Health Check: http://localhost:5001/health")
    print("   - Container Logs: docker logs analyzer-api")

if __name__ == "__main__":
    main()
