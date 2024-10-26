import React, { useState } from 'react';
import '../../styles/CTRHandWritingRecognitionStyles.css';
import GetPhotoBCE from './GetPhotoBCE';

function BCE() {
  const [formData, setFormData] = useState({
    numberOfScorecards: '',
    numberOfRiders: '',
    fastestRiderTime: '',
    heaviestRiderWeight: '',
  });

  const [showGetPhotoBCE, setShowGetPhotoBCE] = useState(false);

  const handleInputChange = (field, event) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };

  const handleContinue = () => {
    if (formData.numberOfRiders) {
      setShowGetPhotoBCE(true);
    } else {
      alert('Please enter the number of riders before continuing.');
    }
  };

  return (
    <div className="bce-container">
      {showGetPhotoBCE ? (
        // Render GetPhotoBCE when user clicks continue
        <GetPhotoBCE numberOfRiders={parseInt(formData.numberOfRiders, 10)} />
      ) : (
        <>
          <div className="input-group">
            <label>Number of scorecards:</label>
            <input
              type="number"
              value={formData.numberOfScorecards}
              onChange={(e) => handleInputChange('numberOfScorecards', e)}
            />
          </div>

          <div className="input-group">
            <label>Number of riders:</label>
            <input
              type="number"
              value={formData.numberOfRiders}
              onChange={(e) => handleInputChange('numberOfRiders', e)}
            />
          </div>

          <div className="input-group">
            <label>Fastest rider time:</label>
            <input
              type="text"
              placeholder="MM:SS" // Placeholder to indicate format
              value={formData.fastestRiderTime}
              onChange={(e) => handleInputChange('fastestRiderTime', e)}
            />
          </div>

          <div className="input-group">
            <label>Heaviest rider weight:</label>
            <input
              type="number"
              value={formData.heaviestRiderWeight}
              onChange={(e) => handleInputChange('heaviestRiderWeight', e)}
            />
          </div>

          <div className="button-container">
            <button className="action-button" onClick={() => console.log("Go Back")}>
              Go back
            </button>
            <button className="action-button" onClick={handleContinue}>
              Continue
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default BCE;
