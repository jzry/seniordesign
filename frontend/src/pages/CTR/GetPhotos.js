import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import UploadIcon from "../../images/upload.png";
import CTRExtractedValues from './CTRExtractedValues.js';
import '../../styles/CTRHandWritingRecognitionStyles.css';

// Handles image upload and submission to the backend
function GetPhotos() {
  const [imageSrc, setImageSrc] = useState(null); // State to store the captured image
  const [imageFile, setImageFile] = useState(null); // State to store the image file for API
  const [extractedData, setExtractedData] = useState(null); // State to store extracted values from API
  const fileInputRef = useRef(null); 
  const navigate = useNavigate();
  const apiUrl = process.env.REACT_APP_API_URL
  // Handles file selection for uploading an image
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageSrc(URL.createObjectURL(file)); // Show the uploaded image
      setImageFile(file); // Store the image file for API submission
    }
  };

  // Clears the current image and allows retaking
  const handleRetakePhoto = () => {
    setImageSrc(null); // Clear the image preview
    setImageFile(null); // Clear the image file
  };

  // Submits the uploaded image to the backend
  const handleSubmit = async (event) => {
    event.preventDefault();

    if (imageFile) {
      const formData = new FormData();
      formData.append('image', imageFile);

      axios.post(apiUrl.concat('/ctr'), formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(response => {
        let ctrData = response.data;
        if (ctrData.error) {
          console.error("The image was not processed correctly")
        } else {
          console.log("Data Retrieved:")
          console.log(ctrData)
          setExtractedData(ctrData)
        }
      })
      .catch(error => {
        console.error('Error uploading file:', error);
      })
    } else {
        console.error("No image to upload.");
    }
  };
  
  const handleGoBack = () => {
    navigate('/'); // Redirect to the home page
  };
  
  return (
    <div className="App">
      {extractedData ? (
        // If we have extracted data, show the CTRHandwritingRecognition component
        <CTRExtractedValues extractedData={extractedData} />
      ) : (
        !imageSrc ? (
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
              <button className="go-back-button" onClick={handleGoBack}>Go Back</button>
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
              <button className="scorecard-button" onClick={(event) => {handleSubmit(event)}}>
                Continue
              </button>
            </div>
          </div>
        )
      )}
    </div>
  );
}

export default GetPhotos;