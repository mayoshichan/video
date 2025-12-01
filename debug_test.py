#!/usr/bin/env python3
"""
Debug test to understand the YouTube search API issues
"""

import requests
import json

BACKEND_URL = "https://portrait-youtube.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

def debug_search_response():
    """Debug the search response to understand the structure"""
    
    queries = ["python programming", "a", "javascript tutorials"]
    
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Testing query: '{query}'")
        print('='*50)
        
        try:
            response = requests.get(
                f"{API_BASE}/search/videos",
                params={"q": query},
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response keys: {list(data.keys())}")
                
                if "items" in data:
                    items = data["items"]
                    print(f"Number of items: {len(items)}")
                    
                    if len(items) > 0:
                        print(f"First item keys: {list(items[0].keys())}")
                        print(f"First item: {json.dumps(items[0], indent=2)}")
                    else:
                        print("No items returned")
                        
                if "error" in data:
                    print(f"Error in response: {data['error']}")
            else:
                print(f"Error response: {response.text}")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    debug_search_response()