import React from 'react';
import { Play } from 'lucide-react';
import { Card } from './ui/card';

const VideoList = ({ videos, onSelectVideo, currentVideoId }) => {
  if (!videos || videos.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <p>No videos found. Try a different search.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {videos.map((video) => (
        <Card
          key={video.id}
          className={`bg-zinc-800 border-zinc-700 hover:bg-zinc-750 transition-all cursor-pointer group ${
            currentVideoId === video.id ? 'ring-2 ring-zinc-500' : ''
          }`}
          onClick={() => onSelectVideo(video.id)}
        >
          <div className="flex gap-3 p-3">
            <div className="relative flex-shrink-0 w-32 h-18 rounded overflow-hidden">
              <img
                src={video.thumbnail}
                alt={video.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all flex items-center justify-center">
                <Play className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-sm font-medium text-white line-clamp-2 group-hover:text-zinc-100 transition-colors">
                {video.title}
              </h3>
              <p className="text-xs text-gray-400 mt-1">{video.channelTitle}</p>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
};

export default VideoList;