import React from 'react';
import './styles.css'; // Ensure this includes global styles (e.g., colors, fonts)

const App = () => {
  return (
    <div className="home-container">
      {/* Image Section */}
      <img src="/spinsync.png" alt="SpinSync" className="spinsync-image" />

      {/* Text Section */}
      <h1 className="welcome-text">Welcome to SpinSync</h1>
      <p className="subtitle">Organize your workout playlists with ease</p>

      {/* Button Section */}
      <button className="login-button">Login with Spotify</button>
    </div>
  );
};

export default App;
