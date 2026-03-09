#!/usr/bin/env python3
"""
Test AI Service integration
"""

import requests
import json
import time

BASE_URL = "http://34.58.51.76:8000"

def test_ai_status():
    """Test AI status endpoint"""
    print("🧪 Test 1: AI Status")
    
    res = requests.get(f"{BASE_URL}/api/v1/ai/status")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    
    data = res.json()
    assert data["available"] == True, "AI should be available"
    assert data["model"] == "gemini-2.5-flash", f"Wrong model: {data['model']}"
    assert "15" in data["rate_limit"], "Rate limit should be 15 req/min"
    
    print("  ✅ AI Status OK")
    print(f"     Model: {data['model']}")
    print(f"     Rate limit: {data['rate_limit']}")

def test_ai_expand_simple():
    """Test AI expand with simple note"""
    print("\n🧪 Test 2: AI Expand (simple note)")
    
    payload = {
        "raw_note": "button unlabeled, NVDA says button only"
    }
    
    start = time.time()
    res = requests.post(
        f"{BASE_URL}/api/v1/ai/expand",
        json=payload,
        timeout=30
    )
    elapsed = time.time() - start
    
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    
    data = res.json()
    assert data["success"] == True, "Should be successful"
    
    result = data["result"]
    
    # Check required fields
    assert "title" in result, "Missing title"
    assert "steps" in result, "Missing steps"
    assert "observed" in result, "Missing observed"
    assert "expected" in result, "Missing expected"
    assert "impact" in result, "Missing impact"
    assert "wcag" in result, "Missing wcag"
    assert "severity" in result, "Missing severity"
    assert "fix" in result, "Missing fix"
    
    # Check WCAG
    assert len(result["wcag"]) > 0, "Should have WCAG criteria"
    wcag_ids = [w["id"] for w in result["wcag"]]
    assert "4.1.2" in wcag_ids, "Should include WCAG 4.1.2"
    
    # Check severity
    assert result["severity"] in ["critical", "serious", "moderate", "minor"], f"Invalid severity: {result['severity']}"
    
    print("  ✅ AI Expand OK")
    print(f"     Title: {result['title']}")
    print(f"     WCAG: {', '.join(wcag_ids)}")
    print(f"     Severity: {result['severity']}")
    print(f"     Time: {elapsed:.1f}s")

def test_ai_expand_with_html():
    """Test AI expand with HTML code"""
    print("\n🧪 Test 3: AI Expand (with HTML)")
    
    payload = {
        "raw_note": "button unlabeled",
        "html_code": "<button onclick='submit()'>Submit</button>"
    }
    
    res = requests.post(
        f"{BASE_URL}/api/v1/ai/expand",
        json=payload,
        timeout=30
    )
    
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    
    data = res.json()
    result = data["result"]
    
    # Check that fix includes code
    assert "button" in result["fix"].lower(), "Fix should mention button"
    assert "aria-label" in result["fix"].lower() or "text" in result["fix"].lower(), "Fix should suggest solution"
    
    print("  ✅ AI Expand with HTML OK")
    print(f"     Fix includes: {result['fix'][:80]}...")

def test_ai_rate_limiting():
    """Test rate limiting (don't exceed 15 req/min)"""
    print("\n🧪 Test 4: Rate Limiting")
    
    # Send 3 requests quickly
    for i in range(3):
        res = requests.post(
            f"{BASE_URL}/api/v1/ai/expand",
            json={"raw_note": f"test {i}"},
            timeout=30
        )
        assert res.status_code == 200, f"Request {i+1} failed"
        print(f"  ✅ Request {i+1}/3 OK")
    
    print("  ✅ Rate limiting OK (no errors)")

def test_dashboard_has_button():
    """Test that dashboard has AI Expand button"""
    print("\n🧪 Test 5: Dashboard UI")
    
    res = requests.get(f"{BASE_URL}/dashboard")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    
    html = res.text
    assert "AI Expand" in html, "Dashboard should have 'AI Expand' button"
    assert "aiExpandNote" in html, "Dashboard should have aiExpandNote() function"
    assert "issue-html" in html, "Dashboard should have HTML code field"
    
    print("  ✅ Dashboard UI OK")
    print("     - AI Expand button: ✅")
    print("     - HTML code field: ✅")
    print("     - JavaScript function: ✅")

if __name__ == "__main__":
    print("=" * 60)
    print("AI SERVICE INTEGRATION TESTS")
    print("=" * 60)
    
    try:
        test_ai_status()
        test_ai_expand_simple()
        test_ai_expand_with_html()
        test_ai_rate_limiting()
        test_dashboard_has_button()
        
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
