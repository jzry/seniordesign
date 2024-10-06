import React, { useState, useRef } from 'react';
import UploadIcon from "../images/upload.png";

function GetPhotos() {
  const [imageSrc, setImageSrc] = useState(null); // State to store the captured image
  const fileInputRef = useRef(null); // Reference to the hidden file input

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageSrc(URL.createObjectURL(file)); // Show the uploaded image
    }
  };

  const handleTakePhoto = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click(); // Programmatically open the file input to trigger camera
    }
  };

  const handleRetakePhoto = () => {
    // Clear the image source to allow for retaking
    setImageSrc(null);
  };

  const handleContinue = () => {
    // Logic to proceed to the next step can be placed here
    console.log("Proceeding to the next step...");
  };

  return (
    <div className="App">
      {!imageSrc ? (
        <div className="button-container">

          {/* Hidden file input to trigger the camera */}
          <input
            type="file"
            accept="image/*"
            capture="environment"
            ref={fileInputRef}
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />

          {/* Upload an image */}
          <div className="icon-button">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              style={{ display: 'none' }}
              id="upload-image"
            />
            <label htmlFor="upload-image" className="icon-button">
              <img src={UploadIcon} alt="upload icon" />
              <p>Upload an image</p>
            </label>
          </div>
        </div>
      ) : (
        <div className="image-fullscreen-container">
          <img src={imageSrc} alt="Preview" className="image-fullscreen" />

          {/* Buttons for retaking or continuing */}
          <div className="action-buttons">
            <button className="scorecard-button" onClick={handleRetakePhoto}>
              Retake Image
            </button>
            <button className="scorecard-button" onClick={handleContinue}>
              Continue
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default GetPhotos;
