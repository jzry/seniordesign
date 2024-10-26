import React, { useState, useEffect } from 'react';
import BCEResults from './BCEResults';
import '../../styles/CTRHandWritingRecognitionStyles.css';

function BCEExtractedValues({ extractedDataList, onGoBackToUpload, heaviestRiderWeight, fastestRiderTime, numberOfRiders }) {
  const [currentRiderIndex, setCurrentRiderIndex] = useState(0); // Index to track the current rider
  const [data, setData] = useState({ ...extractedDataList[currentRiderIndex] }); // Initialize with the first rider's data
  const [step, setStep] = useState(1); // Tracks the current step (1: edit, 2: go back/calculate, 3: show score)
  const [showResults, setShowResults] = useState(false); // State to determine if we should show BCEResults

  // Sync extractedDataList with component state when currentRiderIndex changes
  useEffect(() => {
    if (extractedDataList[currentRiderIndex]) {
      setData({ ...extractedDataList[currentRiderIndex] });
    }
  }, [currentRiderIndex, extractedDataList]);

  const handleInputChange = (key, event) => {
    const newValue = event.target.value;
    setData(prevData => {
      const updatedData = {
        ...prevData,
        [key]: { ...prevData[key], value: newValue }, // Keep the value as string until final submission
      };
      // Update extractedDataList with the new value
      extractedDataList[currentRiderIndex] = updatedData;
      return updatedData;
    });
  };

  const getBorderColor = (confidence) => {
    if (confidence > 0.8) return 'green';
    if (confidence > 0.5) return 'yellow';
    return 'red';
  };

  const handleCalculateScore = () => {
    setShowResults(true); // Show the results after calculation
  };

  const handleGoBack = () => {
    if (step === 2) {
      setStep(1); // Go back to editing the current rider
    } else if (currentRiderIndex > 0) {
      setCurrentRiderIndex(currentRiderIndex - 1);
      setStep(1);
    } else {
      onGoBackToUpload();
    }
  };

  const handleContinue = () => {
    if (currentRiderIndex < extractedDataList.length - 1) {
      setCurrentRiderIndex(currentRiderIndex + 1);
      setStep(1);
    } else {
      setStep(2);
    }
  };

  if (showResults) {
    return <BCEResults extractedDataList={extractedDataList} heaviestRiderWeight={heaviestRiderWeight} />;
  }

  return (
    <div className="container">
      {step === 1 && (
        <div>
          <h3>Rider {currentRiderIndex + 1}</h3>
          {data && Object.keys(data).map((key, index) => (
            <div key={index} className="input-group">
              <label>{key}:</label>
              <input
                type="text"
                value={data[key].value || ""}
                onChange={(event) => handleInputChange(key, event)}
                style={{
                  borderColor: getBorderColor(data[key].confidence),
                }}
              />
            </div>
          ))}
          <div className="button-container">
            <button className="action-button" onClick={handleGoBack}>
              Go Back
            </button>
            <button className="submit-button" onClick={handleContinue}>
              Continue
            </button>
          </div>
        </div>
      )}

      {step === 2 && (
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
    </div>
  );
}

export default BCEExtractedValues;
