import React, { useState, useEffect } from 'react';
import '../../styles/CTRHandWritingRecognitionStyles.css'; // Import the CSS file for styling

function CTRHandwritingRecognition({ extractedData }) {
  const [data, setData] = useState(extractedData); // Initialize with the extracted data

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
      [key]: { ...data[key], value: newValue }
    });
  };

  const getBorderColor = (confidence) => {
    if (confidence > 0.8) return 'green';
    if (confidence > 0.5) return 'yellow';
    return 'red';
  };

  return (
    <div className="container">
      {Object.keys(data).map((key, index) => (
        <div key={index} className="input-group">
          <label>{key}:</label>
          <input
            type="number"
            value={data[key].value}
            onChange={(event) => handleInputChange(key, event)}
            style={{
              borderColor: getBorderColor(data[key].confidence)
            }}
          />
        </div>
      ))}
      <button className="submit-button" onClick={() => console.log("Send data to API")}>
        Calculate Score
      </button>
    </div>
  );
}

export default CTRHandwritingRecognition;
