import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import PhotoOptions from './pages/PhotoOptions';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/photo-options" element={<PhotoOptions />} />
      </Routes>
    </Router>
  );
}

export default App;
