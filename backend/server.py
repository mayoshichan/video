from fastapi import FastAPI, APIRouter, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from youtubesearchpython import VideosSearch


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

@api_router.get("/search/videos")
async def search_videos(q: str = Query(..., description="Search query")):
    """
    Search YouTube videos without API key using youtube-search-python
    """
    try:
        if not q or q.strip() == "":
            return {"items": []}
        
        logger.info(f"Searching for videos with query: {q}")
        
        # Try different search approaches for problematic queries
        items = []
        
        # First try: Direct search
        try:
            videos_search = VideosSearch(q, limit=10)
            results = videos_search.result()
            logger.info(f"Direct search successful for query: {q}")
            
            # Transform results to match frontend format with proper None handling
            if results and 'result' in results and results['result']:
                for video in results['result']:
                    if video is None:
                        continue
                    
                    # Safely extract channel name
                    channel_name = ''
                    if video.get('channel') and isinstance(video.get('channel'), dict):
                        channel_name = video['channel'].get('name', '') or ''
                    
                    # Safely extract thumbnail URL
                    thumbnail_url = ''
                    thumbnails = video.get('thumbnails')
                    if thumbnails and isinstance(thumbnails, list) and len(thumbnails) > 0:
                        first_thumbnail = thumbnails[0]
                        if first_thumbnail and isinstance(first_thumbnail, dict):
                            thumbnail_url = first_thumbnail.get('url', '') or ''
                    
                    # Safely extract description
                    description_text = ''
                    description_snippet = video.get('descriptionSnippet')
                    if description_snippet and isinstance(description_snippet, list) and len(description_snippet) > 0:
                        first_desc = description_snippet[0]
                        if first_desc and isinstance(first_desc, dict):
                            description_text = first_desc.get('text', '') or ''
                    
                    items.append({
                        'id': video.get('id', '') or '',
                        'type': 'video',
                        'title': video.get('title', '') or '',
                        'channelTitle': channel_name,
                        'thumbnail': thumbnail_url,
                        'description': description_text
                    })
        
        except (TypeError, AttributeError) as search_error:
            logger.warning(f"Direct search failed for '{q}': {search_error}")
            
            # Second try: Modified query (remove special characters, limit length)
            try:
                # Clean the query - remove special characters and limit length
                clean_query = ''.join(c for c in q if c.isalnum() or c.isspace()).strip()[:50]
                if clean_query and clean_query != q:
                    logger.info(f"Trying cleaned query: '{clean_query}'")
                    videos_search = VideosSearch(clean_query, limit=5)
                    results = videos_search.result()
                    
                    if results and 'result' in results and results['result']:
                        logger.info(f"Cleaned search successful for: {clean_query}")
                        # Process results same as above but with fewer items
                        for video in results['result'][:5]:
                            if video is None:
                                continue
                            
                            items.append({
                                'id': video.get('id', '') or '',
                                'type': 'video', 
                                'title': video.get('title', '') or '',
                                'channelTitle': video.get('channel', {}).get('name', '') if video.get('channel') else '',
                                'thumbnail': video.get('thumbnails', [{}])[0].get('url', '') if video.get('thumbnails') else '',
                                'description': video.get('descriptionSnippet', [{}])[0].get('text', '') if video.get('descriptionSnippet') else ''
                            })
                            
            except Exception as clean_error:
                logger.warning(f"Cleaned search also failed: {clean_error}")
        
        return {"items": items}
    
    except Exception as e:
        logger.error(f"Error searching videos: {str(e)}")
        return {"items": [], "error": str(e)}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()