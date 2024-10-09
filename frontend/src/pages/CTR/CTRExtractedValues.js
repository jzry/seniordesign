import React, { useState, useEffect } from 'react';
import '../../styles/CTRHandWritingRecognitionStyles.css'; // Import the CSS file for styling

function CTRExtractedValues({ extractedData }) {
  const [data, setData] = useState(extractedData); // Initialize with the extracted data
  const [step, setStep] = useState(1); // Tracks the current step (1: edit, 2: go back/calculate, 3: show score)
  const [totalScore, setTotalScore] = useState(null); // State to store the total score

  // Sync extractedData with component state when it changes
  useEffect(() => {
    if (extractedData) {
      setData(extractedData);
    }
  }, [extractedData]);

  const handleInputChange = (key, event) => {
    const newValue = event.target.value;
    setData({
      ...data,
      [key]: { ...data[key], value: parseInt(newValue, 10) || 0 },
    });
  };

  const getBorderColor = (confidence) => {
    if (confidence > 0.8) return 'green';
    if (confidence > 0.5) return 'yellow';
    return 'red';
  };

  // Handle score calculation (first click shows options, second calculates total score)
  const handleCalculateScore = () => {
    if (step === 2) {
      const sumOfValues = Object.values(data).reduce((acc, item) => acc + (parseInt(item.value, 10) || 0), 0);
      const calculatedScore = 100 - sumOfValues;
      setTotalScore(calculatedScore); // Set the total score
      setStep(3); // Move to the final step (show total score)
    } else {
      setStep(2); // Move to step 2 to show "Go Back" and "Calculate Score"
    }
  };

  // Handle going back to editing
  const handleGoBack = () => {
    setStep(1); // Reset to step 1 to go back to the editable state
  };

  // Handle resetting for new score calculation (back to home or first step)
  const handleCalculateNewScore = () => {
    window.location.reload(); // Simply reloads the page to "start over" (this can be replaced with routing)
  };

  return (
    <div className="container">
      {step === 1 && (
        // Step 1: Editable inputs
        <div>
          {Object.keys(data).map((key, index) => (
            <div key={index} className="input-group">
              <label>{key}:</label>
              <input
                type="number"
                value={data[key].value}
                onChange={(event) => handleInputChange(key, event)}
                style={{
                  borderColor: getBorderColor(data[key].confidence),
                }}
              />
            </div>
          ))}
          <button className="submit-button" onClick={handleCalculateScore}>
            Calculate Score
          </button>
        </div>
      )}

      {step === 2 && (
        // Step 2: Options to go back or calculate the score
        <div className="result-container">
          <p>Would you like to continue editing or calculate your score?</p>
          <button className="action-button" onClick={handleGoBack}>
            Go Back
          </button>
          <button className="action-button" onClick={handleCalculateScore}>
            Calculate Score
          </button>
        </div>
      )}

      {step === 3 && totalScore !== null && (
        // Step 3: Show the total score and calculate new score option
        <div className="result-container">
          <h2>Total Score</h2>
          <h1>{totalScore}</h1>
          <button className="action-button" onClick={handleCalculateNewScore}>
            Calculate New Score
          </button>
        </div>
      )}
    </div>
  );
}

export default CTRExtractedValues;
