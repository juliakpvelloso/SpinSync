import React, { useEffect, useState } from 'react';
import '../styles.css';

const Playlists = () => {
  const [playlists, setPlaylists] = useState([]);

  useEffect(() => {
    // Fetch playlists from the backend
    fetch('/getplaylists')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch playlists');
        }
        return response.json();
      })
      .then((data) => setPlaylists(data))
      .catch((error) => console.error('Error:', error));
  }, []);

  return (
    <div className="playlists-container">
      <h1>Your Playlists</h1>
      <p>Select a playlist to get started</p>
      <div className="grid-container">
        {playlists.map((playlist) => (
          <div key={playlist.id} className="grid-item">
            <img
              src={playlist.image || 'default-placeholder-image.jpg'} // Fallback image
              alt={playlist.name}
              className="playlist-image"
            />
            <p className="playlist-name">{playlist.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Playlists;
