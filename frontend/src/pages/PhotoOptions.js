import React, { useState, useRef } from 'react';
import CameraIcon from "../images/camera.png";
import UploadIcon from "../images/upload.png";
import Webcam from 'react-webcam';

function PhotoOptions() {
  const [imageSrc, setImageSrc] = useState(null); // State to store the captured image
  const [showWebcam, setShowWebcam] = useState(false); // State to show or hide webcam
  const webcamRef = useRef(null); // Reference to the webcam

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Selected file:', file);
      setImageSrc(URL.createObjectURL(file)); // Show the uploaded image
    }
  };

  const handleTakePhoto = () => {
    setShowWebcam(true); // Show the webcam when the button is clicked
  };

  const capturePhoto = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot(); // Capture image from webcam
      setImageSrc(imageSrc); // Set the captured image in state
      setShowWebcam(false); // Hide the webcam after taking a photo
    }
  };

  return (
    <div className="App">
      <div className="button-container">
        {/* Only show the webcam when needed */}
        {showWebcam ? (
          <div className="webcam-container">
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width={320}
              height={240}
            />
            <button className="scorecard-button" onClick={capturePhoto}>
              Capture Photo
            </button>
          </div>
        ) : (
          <>
            {/* Take photo button */}
            <div className="icon-button" onClick={handleTakePhoto}>
              <img src={CameraIcon} alt="camera icon" />
              <p>Take photo</p>
            </div>
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
          </>
        )}
      </div>

      {/* Display the captured or uploaded image */}
      {imageSrc && (
        <div className="image-preview">
          <img src={imageSrc} alt="Preview" />
        </div>
      )}
    </div>
  );
}

export default PhotoOptions;
