import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css';

function Home() {
  return (
    <div className="App">
      <div className="button-container">
        <Link to="/bce">
          <button className="scorecard-button">BCE Scorecard</button>
        </Link>
        <Link to="/ctr">
          <button className="scorecard-button">CTR Scorecard</button>
        </Link>
        {/* <Link to="/corners">
          <button className="scorecard-button">Corner Selection</button>
        </Link> */}
        <Link to="/faq">
          <button className="scorecard-button">FAQ</button>
        </Link>
            <h4>Only JPG, PNG, BMP, TIF, HEIC, and PDF files are accepted for upload.</h4>
            <h4>Only files below 5 Mb are accepted for upload.</h4>
      </div>
    </div>
  );
}

export default Home;
