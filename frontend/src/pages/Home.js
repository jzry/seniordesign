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
      </div>

        {/* <Link to="/corners">
          <button className="scorecard-button">Corner Selection</button>
        </Link> */}

        <div className="container">
        <h4>What image file types are accepted?</h4>
        <p>Only JPG, PNG, BMP, TIF, HEIC, and PDF files are accepted for upload.</p>
        <h4>How do I use the Automated Scorecard Reader?</h4>
        <ol>
            <li>Select which type of scorecard (BCE, CTR) is being read.</li>
                <ul>
                    If BCE, check if it has both sides filled out:
                    <li>If there five riders or less, enter one for "Number of scorecards".</li>
                    <li>If there are more than five riders, enter two for "Number of scorecards".</li>
                </ul>
            <li>For both BCE and CTR, take a photo of the scorecard.</li>
                <ul>
                    <li>If you entered "two" on the previous step, you will be prompted for two photos: the front and back of the BCE page.</li>
                </ul>
            <li>Retake the photo if needed.</li>
            <li>Once submitted, please drag the blue dots to each corner of the scorecard as accurately as possible.</li>
            <li>Once the corners are submitted, check to make sure all values are correct. Click on them and edit if necessary.</li>
                <ul>
                    <li>If the border is <strong>anything except green and solid colored</strong>, it probably needs editing!</li>
                </ul>
            <li>After all fields are validated, click submit.</li>
        </ol>
        <h4>Is there a video tutorial instead?</h4>
        <div className="button-container">
          <a href="https://www.youtube.com/watch?v=VmIr_6LUgsI" target="_blank" rel="noopener noreferrer" className="scorecard">
              Yes, here's the demonstration!
          </a>
        </div>
        <h4>What type of scorecards are accepted?</h4>
          <div className="button-container">
              <a href="https://www.distanceriding.org/wp-content/uploads/2016/09/Judge-Score-Card.pdf" target="_blank" rel="noopener noreferrer" className="scorecard">
                  <img src="https://www.distanceriding.org/wp-content/uploads/2016/09/Judge-Score-Card.pdf" alt="Judge Score Card"/>
              </a>
              <a href="https://aerc.org/wp-content/uploads/2024/04/BestConditionEvaluation2024.pdf" target="_blank" rel="noopener noreferrer" className="scorecard">
                  <img src="https://aerc.org/wp-content/uploads/2024/04/BestConditionEvaluation2024.pdf" alt="Best Condition Evaluation 2024"/>
              </a>
          </div>
      </div>
    </div>
  );
}

export default Home;
