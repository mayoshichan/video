#!/usr/bin/env python3
"""
Backend API Testing Script for YouTube Search Application
Tests the YouTube search API endpoint functionality
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Backend URL from frontend environment
BACKEND_URL = "https://portrait-youtube.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

def test_youtube_search_api():
    """Test the YouTube search API endpoint with different queries"""
    
    print("=" * 60)
    print("TESTING YOUTUBE SEARCH API ENDPOINT")
    print("=" * 60)
    
    # Test cases
    test_queries = [
        "python programming",
        "javascript tutorials"
    ]
    
    all_tests_passed = True
    
    for query in test_queries:
        print(f"\n🔍 Testing search query: '{query}'")
        print("-" * 40)
        
        try:
            # Make API request
            response = requests.get(
                f"{API_BASE}/search/videos",
                params={"q": query},
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ FAILED: Expected status 200, got {response.status_code}")
                print(f"Response: {response.text}")
                all_tests_passed = False
                continue
            
            # Parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                print(f"❌ FAILED: Invalid JSON response - {e}")
                print(f"Response text: {response.text}")
                all_tests_passed = False
                continue
            
            # Check if response has 'items' array
            if "items" not in data:
                print(f"❌ FAILED: Response missing 'items' array")
                print(f"Response keys: {list(data.keys())}")
                all_tests_passed = False
                continue
            
            items = data["items"]
            
            if not isinstance(items, list):
                print(f"❌ FAILED: 'items' is not an array")
                all_tests_passed = False
                continue
            
            print(f"✅ Found {len(items)} video results")
            
            if len(items) == 0:
                print("⚠️  WARNING: No videos returned for this query")
                continue
            
            # Test first few videos for required fields
            required_fields = ["id", "type", "title", "channelTitle", "thumbnail", "description"]
            
            for i, video in enumerate(items[:3]):  # Test first 3 videos
                print(f"\n  📹 Video {i+1}:")
                
                missing_fields = []
                for field in required_fields:
                    if field not in video:
                        missing_fields.append(field)
                    else:
                        # Check if field has meaningful content
                        value = video[field]
                        if field == "id":
                            print(f"    ID: {value}")
                            if not value or len(str(value).strip()) == 0:
                                print(f"    ⚠️  WARNING: Empty video ID")
                        elif field == "type":
                            print(f"    Type: {value}")
                            if value != "video":
                                print(f"    ⚠️  WARNING: Expected type 'video', got '{value}'")
                        elif field == "title":
                            print(f"    Title: {value[:50]}{'...' if len(str(value)) > 50 else ''}")
                        elif field == "channelTitle":
                            print(f"    Channel: {value}")
                        elif field == "thumbnail":
                            if value:
                                print(f"    Thumbnail: {value[:50]}{'...' if len(str(value)) > 50 else ''}")
                            else:
                                print(f"    Thumbnail: (empty)")
                        elif field == "description":
                            if value:
                                print(f"    Description: {value[:50]}{'...' if len(str(value)) > 50 else ''}")
                            else:
                                print(f"    Description: (empty)")
                
                if missing_fields:
                    print(f"    ❌ MISSING FIELDS: {missing_fields}")
                    all_tests_passed = False
                else:
                    print(f"    ✅ All required fields present")
            
            # Check if video IDs look like valid YouTube IDs
            valid_id_count = 0
            for video in items[:5]:  # Check first 5 videos
                video_id = video.get("id", "")
                if video_id and len(str(video_id).strip()) >= 10:  # YouTube IDs are typically 11 characters
                    valid_id_count += 1
            
            print(f"\n  📊 Valid-looking video IDs: {valid_id_count}/{min(5, len(items))}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ FAILED: Network error - {e}")
            all_tests_passed = False
        except Exception as e:
            print(f"❌ FAILED: Unexpected error - {e}")
            all_tests_passed = False
    
    return all_tests_passed

def test_edge_cases():
    """Test edge cases for the YouTube search API"""
    
    print("\n" + "=" * 60)
    print("TESTING EDGE CASES")
    print("=" * 60)
    
    edge_cases = [
        ("", "Empty query"),
        ("   ", "Whitespace only query"),
        ("a", "Single character query"),
        ("nonexistentquerythatshouldhavenovideos12345", "Query with likely no results")
    ]
    
    all_tests_passed = True
    
    for query, description in edge_cases:
        print(f"\n🧪 Testing: {description}")
        print(f"Query: '{query}'")
        print("-" * 40)
        
        try:
            response = requests.get(
                f"{API_BASE}/search/videos",
                params={"q": query},
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if "items" in data:
                    print(f"✅ Returned {len(data['items'])} items")
                else:
                    print(f"❌ FAILED: Missing 'items' in response")
                    all_tests_passed = False
            else:
                print(f"⚠️  Non-200 status code: {response.status_code}")
                
        except Exception as e:
            print(f"❌ FAILED: Error - {e}")
            all_tests_passed = False
    
    return all_tests_passed

def main():
    """Main test runner"""
    
    print("🚀 Starting Backend API Tests")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"API Base: {API_BASE}")
    
    # Test basic connectivity
    print("\n" + "=" * 60)
    print("TESTING BASIC CONNECTIVITY")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE}/", timeout=10)
        print(f"Root endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Backend is accessible")
        else:
            print(f"⚠️  Backend returned status {response.status_code}")
    except Exception as e:
        print(f"❌ FAILED: Cannot connect to backend - {e}")
        return False
    
    # Run main tests
    main_tests_passed = test_youtube_search_api()
    edge_tests_passed = test_edge_cases()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if main_tests_passed and edge_tests_passed:
        print("🎉 ALL TESTS PASSED")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        if not main_tests_passed:
            print("  - Main YouTube search tests failed")
        if not edge_tests_passed:
            print("  - Edge case tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)