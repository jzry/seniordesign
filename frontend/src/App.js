import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import GetPhotos from './pages/GetPhotos';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/get-photos" element={< GetPhotos/>} />
      </Routes>
    </Router>
  );
}

export default App;
