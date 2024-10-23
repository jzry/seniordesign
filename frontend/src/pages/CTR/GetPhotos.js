import React, { useState, useRef } from 'react';
import axios from 'axios';
import UploadIcon from "../../images/upload.png";
import CTRExtractedValues from './CTRExtractedValues.js'; // Import the component

function GetPhotos() {
  const [imageSrc, setImageSrc] = useState(null); // State to store the captured image
  const [imageFile, setImageFile] = useState(null); // State to store the image file for API
  const [extractedData, setExtractedData] = useState(null); // State to store extracted values from API
  const fileInputRef = useRef(null); // Reference to the hidden file input

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageSrc(URL.createObjectURL(file)); // Show the uploaded image
      setImageFile(file); // Store the image file for API submission
    }
  };

  const handleRetakePhoto = () => {
    setImageSrc(null); // Clear the image preview
    setImageFile(null); // Clear the image file
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('image', imageFile);

    try {
      const response = await axios.post('http://localhost:8080/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };


  const handleContinue = async () => {
    if (imageFile) {
      const formData = new FormData();
      formData.append('image', imageFile);

      try {
        // Simulate the API response with a delay
        const result = await new Promise((resolve) => {
          setTimeout(() => {
            resolve({
              "Pulse Before Trot Out": { value: 4, confidence: 0.9 },
              "Pulse After Trot Out": { value: 3, confidence: 0.75 },
              "Mucous Membrane": { value: 5, confidence: 0.95 },
              "Capillary Refill": { value: 2, confidence: 0.7 },
              "Skin Pinch": { value: 0, confidence: 0.4 },
              "Jugular Vein Refill": { value: 2, confidence: 0.9 },
              "Anal Tone": { value: -1, confidence: 0.3 },
              "Muscle Tone": { value: -2, confidence: 0.6 },
              "Unwillingness to trot": { value: -5, confidence: 0.85 },
              "Tendons, Ligaments, Joints, Filings": { value: -20, confidence: 0.7 },
              "Interferences": { value: -5, confidence: 0.9 },
              "Grade 1": { value: -10, confidence: 0.95 },
              "Grade 2": { value: -11, confidence: 0.92 },
              "Back Tenderness": { value: -5, confidence: 0.9 },
              "Tack Area": { value: -4, confidence: 0.85 },
              "Hold on Trail": { value: 0, confidence: 0.9 },
              "Time Penalty": { value: -1, confidence: 0.9 }
            });
          }, 100); // Simulated delay of 1 second
        });
  
        console.log('Image processed successfully:', result);
  
        // Assuming result contains extracted values and confidence levels
        setExtractedData(result); // Store the extracted values
  
      } catch (error) {
        console.error('Error uploading image:', error);
      }
    } else {
      console.error("No image to upload.");
    }
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
              <button className="scorecard-button" onClick={(event) => {handleSubmit(event); handleContinue()}}>
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