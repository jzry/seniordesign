import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import GetPhotos from './pages/CTR/GetPhotos';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ctr" element={< GetPhotos/>} />
      </Routes>
    </Router>
  );
}

export default App;
