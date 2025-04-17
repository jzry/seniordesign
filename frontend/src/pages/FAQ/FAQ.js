import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../../styles/CTRHandWritingRecognitionStyles.css';

function FAQ(){
    const navigate = useNavigate();
    const handleGoBack = () => {
        navigate('/');
      }

    return (
        <div className="container">
            <h4>How do I use the Automated Scorecard Reader?</h4>
            <ol>
                <li>Select which type of scorecard (BCE, CTR) is being read.</li>
                    <ul>
                        If BCE, check how many pages are filled out:
                        <li>If there five riders or less, enter one for "Number of scorecards".</li>
                        <li>If there are more than five riders, enter two for "Number of scorecards".</li>
                    </ul>
                <li>For both BCE and CTR, take a photo of the scorecard, with all corners visible.</li>
                    <ul>
                        <li>If you entered "two" on the previous step, you will be prompted for two photos: one of each filled out page with the rider scores.</li>
                    </ul>
                <li>Retake the photo if needed.</li>
                <li>Once submitted, please drag the blue dots to each corner of the scorecard as accurately as possible.</li>
                <li>Once the corners are submitted, check to make sure all values are correct. Click on them and edit if necessary.</li>
                    <ul>
                        The borders will vary based on how accurately the digits were read as follows:
                        <li style={{padding: "15px"}}> <strong style={{borderRadius: "10px", border: "2px solid green", padding: "8px", 
                            boxShadow: "2px 2px 10px rgba(0, 0, 0, 0.1)",
                            }}>Accuracy &ge; 95%</strong></li>
                        <li style={{padding: "15px"}}><strong style={{borderRadius: "10px", border: "2px dashed gold", padding: "8px", 
                            boxShadow: "2px 2px 10px rgba(0, 0, 0, 0.1)",
                            }}>95% &gt; Accuracy &ge; 85%</strong></li>
                        <li style={{padding: "15px"}}><strong style={{borderRadius: "10px", border: "2px dotted red", padding: "8px", 
                            boxShadow: "2px 2px 10px rgba(0, 0, 0, 0.1)",
                            }}>Accuracy &lt; 85%</strong></li>

                        <li>If the border is <strong>anything except green and solid colored</strong>, it probably needs editing!</li>
                    </ul>
                <li>After all fields are validated, click submit.</li>
                <li>Contemplate your final calculation; saying "hmmm!" while stroking your chin is greatly encouraged.</li>
            </ol>
            <h4>Is there a video tutorial instead?</h4>
            <div className="button-container">
            <a href="https://www.youtube.com/watch?v=VmIr_6LUgsI" target="_blank" rel="noopener noreferrer" className="scorecard">
                Yes, here's the demonstration!
            </a>
            </div>
            <h4>What type of scorecards are accepted?</h4>
            <div className="button-container">
              <a href="https://www.distanceriding.org/wp-content/uploads/2016/09/Judge-Score-Card.pdf" target="_blank" rel="noopener noreferrer" >
                  <img src="https://www.distanceriding.org/wp-content/uploads/2016/09/Judge-Score-Card.pdf" alt="Judge Score Card" className="scorecard"/>
              </a>
              <a href="https://aerc.org/wp-content/uploads/2024/04/BestConditionEvaluation2024.pdf" target="_blank" rel="noopener noreferrer" >
                  <img src="https://aerc.org/wp-content/uploads/2024/04/BestConditionEvaluation2024.pdf" alt="Best Condition Evaluation 2024" className="scorecard"/>
              </a>
            </div>
            <h4>What image file types are accepted?</h4>
            <p>Only JPG, PNG, BMP, TIF, HEIC, and PDF files are accepted for upload.</p>
            <h4>What size of image file types are accepted?</h4>
            <p>Only files below 5 Mb are accepted for upload.</p>
            <div className="button-container">
                <button className="action-button" onClick={handleGoBack}>
                Go back
                </button>
            </div>
        </div>
    );
}
export default FAQ;