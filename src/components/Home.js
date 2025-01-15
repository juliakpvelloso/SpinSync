import React from 'react';
import '../styles.css'; // Ensure this includes global styles (e.g., colors, fonts)

const App = () => {
  const handleLogin = () => {
    window.location.href = '/login'; // Redirect to the backend login route
  };
  return (
    <div className="home-container">
      {/* Image Section */}
      <img src="/spinsync.png" alt="SpinSync" className="spinsync-image" />

      {/* Text Section */}
      <h1 className="welcome-text">Welcome to SpinSync</h1>
      <p className="subtitle">Organize your workout playlists with ease</p>

      {/* Button Section */}
      <button className="login-button" onClick={handleLogin}>
        Login with Spotify
      </button>
    </div>
  );
};

export default App;
