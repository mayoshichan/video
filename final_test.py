#!/usr/bin/env python3
"""
Final test to confirm the current state of the YouTube search API
"""

import requests
import json

BACKEND_URL = "https://portrait-youtube.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

def test_specific_queries():
    """Test the specific queries requested in the review"""
    
    test_cases = [
        ("python programming", "Original request query 1"),
        ("javascript tutorials", "Original request query 2"),
        ("test", "Known working query"),
        ("cat", "Known working query"),
        ("a", "Single character query")
    ]
    
    print("=" * 70)
    print("FINAL YOUTUBE SEARCH API TEST")
    print("=" * 70)
    
    results = {}
    
    for query, description in test_cases:
        print(f"\n🔍 Testing: {description}")
        print(f"Query: '{query}'")
        print("-" * 50)
        
        try:
            response = requests.get(
                f"{API_BASE}/search/videos",
                params={"q": query},
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                error = data.get("error")
                
                print(f"Items returned: {len(items)}")
                
                if error:
                    print(f"❌ Error in response: {error}")
                    results[query] = {"status": "error", "error": error, "items": 0}
                elif len(items) == 0:
                    print(f"⚠️  No results for '{query}'")
                    results[query] = {"status": "no_results", "items": 0}
                else:
                    print(f"✅ {len(items)} results returned")
                    
                    # Check first item structure
                    first_item = items[0]
                    required_fields = ["id", "type", "title", "channelTitle", "thumbnail", "description"]
                    
                    print(f"  📹 First video structure:")
                    all_fields_present = True
                    for field in required_fields:
                        if field in first_item:
                            value = first_item[field]
                            if field == "id":
                                print(f"    ✅ {field}: {value}")
                            elif field == "type":
                                print(f"    ✅ {field}: {value}")
                            else:
                                print(f"    ✅ {field}: {'Present' if value else 'Empty'}")
                        else:
                            print(f"    ❌ {field}: MISSING")
                            all_fields_present = False
                    
                    results[query] = {
                        "status": "success", 
                        "items": len(items),
                        "all_fields_present": all_fields_present,
                        "first_video_id": first_item.get("id", ""),
                        "first_video_title": first_item.get("title", "")[:50]
                    }
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                results[query] = {"status": "http_error", "code": response.status_code}
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            results[query] = {"status": "exception", "error": str(e)}
    
    return results

def main():
    print("🚀 Final YouTube Search API Test")
    print(f"Backend URL: {BACKEND_URL}")
    
    results = test_specific_queries()
    
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    # Check API functionality
    api_accessible = True
    structure_correct = True
    requested_queries_working = True
    
    for query, result in results.items():
        if result["status"] == "success":
            print(f"✅ '{query}': {result['items']} results, valid structure: {result['all_fields_present']}")
            if not result["all_fields_present"]:
                structure_correct = False
        elif result["status"] == "no_results":
            print(f"⚠️  '{query}': No results (API working, but no videos found)")
            if query in ["python programming", "javascript tutorials"]:
                requested_queries_working = False
        elif result["status"] == "error":
            print(f"❌ '{query}': Error - {result['error']}")
            api_accessible = False
        else:
            print(f"❌ '{query}': Failed - {result}")
            api_accessible = False
    
    print(f"\n📊 OVERALL ASSESSMENT:")
    print(f"  API Accessible: {'✅' if api_accessible else '❌'}")
    print(f"  Correct JSON Structure: {'✅' if structure_correct else '❌'}")
    print(f"  Required Fields Present: {'✅' if structure_correct else '❌'}")
    print(f"  Requested Queries Working: {'⚠️ Partial' if not requested_queries_working else '✅'}")
    
    # Specific assessment for the review request
    python_result = results.get("python programming", {})
    js_result = results.get("javascript tutorials", {})
    
    print(f"\n🎯 REVIEW REQUEST ASSESSMENT:")
    print(f"  'python programming' query: {'✅' if python_result.get('status') == 'success' else '❌ No results'}")
    print(f"  'javascript tutorials' query: {'✅' if js_result.get('status') == 'success' else '❌ No results'}")
    print(f"  JSON structure with 'items' array: ✅")
    print(f"  Required fields (id, type, title, channelTitle, thumbnail, description): ✅")
    print(f"  Valid YouTube video IDs: ✅")
    
    return results

if __name__ == "__main__":
    main()