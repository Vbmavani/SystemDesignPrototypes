from fastapi import FastAPI, Request, Response, HTTPException
from typing import Optional
import os
import json
import hashlib
import requests

app = FastAPI()

# Set up cache directory
cache_dir = "cdn"
os.makedirs(cache_dir, exist_ok=True)

# Origin mappings
origin_map = {
    "127.0.0.1:8001": "http://localhost:8002/"  
}

def cache_get(url_hash: str) -> Optional[Response]:
    """Retrieve a cached response if available."""
    cache_path = os.path.join(cache_dir, url_hash)
    print('cache_path',cache_path)
    if not os.path.exists(cache_path):
        return None
    
    with open(cache_path, "r") as f:
        data = json.load(f)
    return Response(content=data["text"], media_type="application/json")

def cache_put(url_hash: str, response: Response):
    """Cache the response."""
    cache_path = os.path.join(cache_dir, url_hash)
    with open(cache_path, "w") as f:
        json.dump({"text": response.text}, f)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    # Determine the origin base URL
    origin_key = f"{request.client.host}:{request.url.port}"

    print(origin_key)

    origin_base = origin_map.get(origin_key)
    if not origin_base:
        return Response(f"Unknown origin: {request.client.host}", status_code=404)
    
    # Build the origin URL
    origin_url = f"{origin_base}/{path}"
    url_hash = hashlib.md5(origin_url.encode()).hexdigest()
    
    # Check for cached response
    cached_response = cache_get(url_hash)
    if cached_response:
        return cached_response
    
    
    # Forward request to origin server
    try:
        origin_response = requests.request(
            method=request.method,
            url=origin_url,
            headers=request.headers,
            data=await request.body() if request.method in ["POST", "PUT"] else None
        )
        origin_response.raise_for_status()
        
        print('cashe::',url_hash,origin_response.text)
        # Cache and return the response
        cache_put(url_hash, origin_response)
        return Response(content=origin_response.text, status_code=origin_response.status_code)
    
    except requests.RequestException as e:
        return Response(f"Error from origin: {str(e)}", status_code=origin_response.status_code if 'origin_response' in locals() else 500)

