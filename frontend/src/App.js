import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Signup from './pages/Signup/Signup';
import Login from './pages/Login/Login';
import GetPhotos from './pages/CTR/GetPhotos';
import BCE from './pages/BCE/BCE';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/ctr" element={< GetPhotos/>} />
        <Route path="/bce" element={< BCE/>} />
      </Routes>
    </Router>
  );
}

export default App;
