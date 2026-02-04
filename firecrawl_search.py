#!/usr/bin/env python3
"""
FireCrawl Search & Scrape Integration
Wrapper for FireCrawl /v2/search with intelligent fallback to OpenClaw defaults
"""

import os
import sys
import json
import time
from typing import Optional
import urllib.request
import urllib.error

# Configuration
FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY")
if not FIRECRAWL_API_KEY:
    raise ValueError(
        "FIRECRAWL_API_KEY environment variable not set!\n"
        "Please set it: export FIRECRAWL_API_KEY='your-api-key'"
    )
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev"
REQUEST_TIMEOUT = 30
MAX_SCRAPE_RETRIES = 2

def make_request(endpoint: str, payload: dict, timeout: int = REQUEST_TIMEOUT) -> Optional[dict]:
    """Make HTTP POST request to FireCrawl API with proper auth headers"""
    url = f"{FIRECRAWL_BASE_URL}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        print(f"FireCrawl HTTP Error {e.code}: {error_data}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"FireCrawl Connection Error: {e.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"FireCrawl Response JSON Error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"FireCrawl Request Error: {e}", file=sys.stderr)
        return None

def search(query: str, limit: int = 5, scrape: bool = False) -> dict:
    """
    Search using FireCrawl /v2/search endpoint
    
    Args:
        query: Search query
        limit: Max results to return
        scrape: If True, extract markdown from each result
    
    Returns:
        dict with 'success', 'results', and optional 'error'
    """
    
    payload = {
        "query": query,
        "limit": limit,
        "sources": ["web"]
    }
    
    if scrape:
        payload["scrapeOptions"] = {
            "formats": ["markdown"],
            "onlyMainContent": True
        }
    
    print(f"FireCrawl Search - Query: {query} (mode: {'scrape' if scrape else 'search'})")
    
    response = make_request("/v2/search", payload)
    
    if not response:
        return {
            "success": False,
            "error": "FireCrawl API request failed",
            "fallback": "Use OpenClaw web_search instead"
        }
    
    if response.get("success") is False:
        error_msg = response.get("error", "Unknown error")
        print(f"FireCrawl Error: {error_msg}", file=sys.stderr)
        return {
            "success": False,
            "error": error_msg,
            "fallback": "Use OpenClaw web_search instead"
        }
    
    # Parse results - FireCrawl returns nested in data.web
    results = []
    
    # FireCrawl /v2/search returns results in data.web array
    data = response.get("data", {})
    raw_results = data.get("web", [])
    
    # Fallback options
    if not raw_results:
        raw_results = response.get("results", [])
    if not raw_results and isinstance(response, list):
        raw_results = response
    
    if not raw_results:
        return {
            "success": True,
            "results": [],
            "count": 0
        }
    
    for item in raw_results[:limit]:
        if not isinstance(item, dict):
            continue
        
        result_item = {
            "position": item.get("position"),
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
        }
        
        # If scrape mode, include markdown content
        if scrape and "markdown" in item:
            result_item["markdown_content"] = item["markdown"]
        
        if result_item.get("url"):  # Only add if we have a URL
            results.append(result_item)
    
    return {
        "success": True,
        "results": results,
        "count": len(results),
        "mode": "scrape" if scrape else "search"
    }

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: firecrawl_search.py <query> [--scrape] [--limit N]")
        sys.exit(1)
    
    query = sys.argv[1]
    scrape_mode = "--scrape" in sys.argv
    
    # Extract limit if provided
    limit = 5
    if "--limit" in sys.argv:
        try:
            idx = sys.argv.index("--limit")
            limit = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            pass
    
    result = search(query, limit=limit, scrape=scrape_mode)
    
    # Output as JSON for parsing
    print(json.dumps(result, indent=2))
    
    if not result.get("success"):
        sys.exit(1)

if __name__ == "__main__":
    main()
