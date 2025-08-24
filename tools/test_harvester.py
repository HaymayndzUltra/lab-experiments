#!/usr/bin/env python3
import urllib.request
import urllib.error
import ssl
import time

def test_url(url):
    print(f"\n=== Testing {url} ===")
    
    # Method 1: urllib with custom context
    try:
        print("Method 1: urllib with custom SSL context")
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers={'User-Agent': 'TeteyHarvester/1.0'})
        with urllib.request.urlopen(req, timeout=10, context=context) as response:
            print(f"Status: {response.status}")
            print(f"Content length: {len(response.read())}")
            return True
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    # Method 2: Simple urllib
    try:
        print("Method 2: Simple urllib")
        req = urllib.request.Request(url, headers={'User-Agent': 'TeteyHarvester/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"Status: {response.status}")
            print(f"Content length: {len(response.read())}")
            return True
    except Exception as e:
        print(f"Method 2 failed: {e}")
    
    return False

if __name__ == "__main__":
    urls = [
        "https://cursor.directory/rules",
        "https://cursor.directory/rules/popular",
        "https://cursor.directory/rules/official"
    ]
    
    for url in urls:
        success = test_url(url)
        if success:
            print("✅ SUCCESS")
        else:
            print("❌ FAILED")
        time.sleep(1)
