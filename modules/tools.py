import datetime
import json
import os
import platform
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

# --- Existing System Tools ---

def get_system_info():
    """Returns basic system platform and hardware information."""
    return json.dumps({
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version()
    })

def get_current_time():
    """Returns the current date, time, and timezone."""
    now = datetime.datetime.now()
    return json.dumps({
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "day": now.strftime("%A")
    })

# --- New Web Tools ---

def web_search(query: str, max_results: int = 5):
    """Searches the internet via DuckDuckGo and returns top search results."""
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "link": r.get("href"),
                    "snippet": r.get("body")
                })
        return json.dumps(results)
    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})

def scrape_webpage(url: str):
    """Fetches text content from a given web URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return json.dumps({"error": f"Failed to fetch page. HTTP Status: {response.status_code}"})
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Strip script and style tags
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.decompose()
            
        text = soup.get_text(separator=" ", strip=True)
        # Limit scraped output size to save context memory tokens
        truncated_text = text[:3000] + ("..." if len(text) > 3000 else "")
        
        return json.dumps({"url": url, "content": truncated_text})
    except Exception as e:
        return json.dumps({"error": f"Scraping failed: {str(e)}"})

# --- Tool Schemas for Gemini ---

AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_system_info",
            "description": "Get details about the host system environment (OS, platform, architecture).",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and system time.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the live web for real-time information, news, current events, or topics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string to submit to the search engine."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_webpage",
            "description": "Extract text content from a specific web page URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The target URL to scrape."
                    }
                },
                "required": ["url"]
            }
        }
    }
]

# Map tool names directly to Python functions
TOOL_MAP = {
    "get_system_info": get_system_info,
    "get_current_time": get_current_time,
    "web_search": web_search,
    "scrape_webpage": scrape_webpage
}