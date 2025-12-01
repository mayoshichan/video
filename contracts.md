# API Contracts & Integration Plan

## Backend Implementation

### 1. YouTube Search Package
- **Package**: `youtube-search-api` (npm)
- **No API key required**: Uses web scraping/reverse engineering
- **Features**: Search videos, playlists, and channels

### 2. API Endpoints

#### GET /api/search/videos
**Query Parameters:**
- `q` (string, required): Search query

**Response:**
```json
{
  "items": [
    {
      "id": "video_id",
      "type": "video",
      "title": "Video Title",
      "channelTitle": "Channel Name",
      "thumbnail": "thumbnail_url",
      "description": "Video description"
    }
  ]
}
```

### 3. Frontend Changes
**Remove:**
- `mock.js` file (currently provides mock search data)
- Mock data imports from `Home.jsx`

**Update:**
- `Home.jsx`: Replace `searchVideos()` function to call `/api/search/videos` endpoint
- Use axios for API calls
- Handle loading and error states

### 4. Data Mapping
**youtube-search-api response → Frontend format:**
- `id.videoId` → `id`
- `snippet.title` → `title`
- `snippet.channelTitle` → `channelTitle`
- `thumbnail.thumbnails.medium.url` → `thumbnail`
- `snippet.description` → `description`

### 5. Implementation Steps
1. Install `youtube-search-api` in backend
2. Create search route in `server.py`
3. Update frontend to use real API
4. Remove mock data
5. Test search functionality
