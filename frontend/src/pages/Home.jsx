import React, { useState, useEffect } from 'react';
import { Youtube, Loader2 } from 'lucide-react';
import axios from 'axios';
import SearchBar from '../components/SearchBar';
import VideoList from '../components/VideoList';
import YouTubePlayer from '../components/YouTubePlayer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [currentVideoId, setCurrentVideoId] = useState('dQw4w9WgXcQ'); // Default video
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load initial results
  useEffect(() => {
    handleSearch('gaming');
  }, []);

  const handleSearch = async (query) => {
    if (!query || query.trim() === '') {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`${API}/search/videos`, {
        params: { q: query }
      });

      const results = response.data.items || [];
      setSearchResults(results);
      
      if (results.length > 0) {
        setCurrentVideoId(results[0].id);
      }
    } catch (err) {
      console.error('Search error:', err);
      setError('Failed to search videos. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectVideo = (videoId) => {
    setCurrentVideoId(videoId);
  };

  return (
    <div className="min-h-screen bg-zinc-900 flex items-center justify-center p-4">
      {/* 9:16 Container - Portrait Phone Layout */}
      <div 
        className="w-full max-w-md bg-black shadow-2xl overflow-hidden"
        style={{ aspectRatio: '9/16' }}
      >
        <div className="h-full flex flex-col">
          {/* Header */}
          <div className="bg-zinc-900 px-4 py-3 border-b border-zinc-800">
            <div className="flex items-center gap-2 mb-3">
              <Youtube className="w-6 h-6 text-red-600" />
              <h1 className="text-lg font-bold text-white">YouTube Player</h1>
            </div>
            <SearchBar onSearch={handleSearch} />
          </div>

          {/* Video Player - 16:9 aspect ratio */}
          <div className="bg-black">
            <YouTubePlayer videoId={currentVideoId} />
          </div>

          {/* Video List - Scrollable */}
          <div className="flex-1 overflow-y-auto bg-zinc-900 p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-gray-300">Search Results</h2>
              {loading && (
                <Loader2 className="w-4 h-4 text-gray-400 animate-spin" />
              )}
            </div>
            
            {error && (
              <div className="text-red-400 text-sm mb-3 p-3 bg-red-900/20 rounded">
                {error}
              </div>
            )}
            
            <VideoList
              videos={searchResults}
              onSelectVideo={handleSelectVideo}
              currentVideoId={currentVideoId}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;