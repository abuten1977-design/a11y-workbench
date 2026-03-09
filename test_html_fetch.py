#!/usr/bin/env python3
"""
Test HTML fetch functionality
"""

import requests

BASE_URL = "http://34.58.51.76:8000"

def test_proxy_endpoint():
    """Test proxy endpoint with clean URL"""
    print("🧪 Test 1: Proxy with clean URL")
    
    url = "http://example.com"
    res = requests.get(f"{BASE_URL}/api/v1/proxy?url={url}", timeout=15)
    
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "Example Domain" in res.text, "Should contain example.com content"
    
    print("  ✅ Proxy works with clean URL")

def test_proxy_with_whitespace():
    """Test proxy endpoint with URL containing whitespace"""
    print("\n🧪 Test 2: Proxy with whitespace in URL")
    
    # URL with trailing spaces (like from database)
    url = "http://example.com     "
    res = requests.get(f"{BASE_URL}/api/v1/proxy?url={url}", timeout=15)
    
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "Example Domain" in res.text, "Should handle whitespace and fetch content"
    
    print("  ✅ Proxy handles whitespace correctly")

def test_fetch_dashboard_html():
    """Test fetching dashboard HTML"""
    print("\n🧪 Test 3: Fetch dashboard HTML")
    
    url = "http://34.58.51.76:8000/dashboard"
    res = requests.get(f"{BASE_URL}/api/v1/proxy?url={url}", timeout=15)
    
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "A11y Workbench" in res.text, "Should contain dashboard content"
    
    print("  ✅ Can fetch dashboard HTML")
    print(f"     HTML size: {len(res.text)} characters")

if __name__ == "__main__":
    print("=" * 60)
    print("HTML FETCH TESTS")
    print("=" * 60)
    
    try:
        test_proxy_endpoint()
        test_proxy_with_whitespace()
        test_fetch_dashboard_html()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
