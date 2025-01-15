import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home'; // Home page
import Playlists from './components/Playlists'; // Playlists page
import '../src/styles.css'; // Global styles

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} /> {/* Home Page */}
        <Route path="/playlists" element={<Playlists />} /> {/* Playlists Page */}
      </Routes>
    </Router>
  );
};

export default App;
