import React, { useEffect, useRef, useState } from 'react';

const YouTubePlayer = ({ videoId }) => {
  const playerRef = useRef(null);
  const [player, setPlayer] = useState(null);

  useEffect(() => {
    // Load YouTube IFrame API
    if (!window.YT) {
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      const firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    // Initialize player when API is ready
    const initPlayer = () => {
      if (window.YT && window.YT.Player && playerRef.current) {
        const newPlayer = new window.YT.Player(playerRef.current, {
          videoId: videoId,
          playerVars: {
            autoplay: 1,
            modestbranding: 1,
            rel: 0
          }
        });
        setPlayer(newPlayer);
      }
    };

    if (window.YT && window.YT.Player) {
      initPlayer();
    } else {
      window.onYouTubeIframeAPIReady = initPlayer;
    }
  }, []);

  // Update video when videoId changes
  useEffect(() => {
    if (player && player.loadVideoById) {
      player.loadVideoById(videoId);
    }
  }, [videoId, player]);

  return (
    <div className="w-full bg-black flex items-center justify-center overflow-hidden" style={{ height: '400px' }}>
      <div 
        className="relative"
        style={{
          transform: 'rotate(90deg)',
          transformOrigin: 'center center',
          width: '400px',
          height: '300px'
        }}
      >
        <div ref={playerRef} className="w-full h-full" />
      </div>
    </div>
  );
};

export default YouTubePlayer;