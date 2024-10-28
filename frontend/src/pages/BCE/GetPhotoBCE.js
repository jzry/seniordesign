import React, { useState, useRef } from 'react';
import UploadIcon from "../../images/upload.png";
import BCEExtractedValues from './BCEExtractedValues';
import '../../styles/CTRHandWritingRecognitionStyles.css';

function GetPhotoBCE({ numberOfRiders, fastestRiderTime, heaviestRiderWeight }) {
  const [imageSrc1, setImageSrc1] = useState(null);
  const [imageSrc2, setImageSrc2] = useState(null);
  const [imageFile1, setImageFile1] = useState(null);
  const [imageFile2, setImageFile2] = useState(null);
  const [extractedDataList, setExtractedDataList] = useState([]);
  const [currentStep, setCurrentStep] = useState(1);
  const fileInputRef = useRef(null);

  const isTwoPhotosRequired = numberOfRiders > 5;

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      if (currentStep === 1) {
        setImageSrc1(imageUrl);
        setImageFile1(file);
      } else {
        setImageSrc2(imageUrl);
        setImageFile2(file);
      }
    }
  };

  const handleRetakePhoto = () => {
    if (currentStep === 1) {
      setImageSrc1(null);
      setImageFile1(null);
    } else {
      setImageSrc2(null);
      setImageFile2(null);
    }
  };

  const handleContinue = async () => {
    if ((currentStep === 1 && imageFile1) || (currentStep === 2 && imageFile2)) {
      if (isTwoPhotosRequired && currentStep === 1) {
        // Move to step 2 to capture the second photo for the current group
        setCurrentStep(2);
      } else {
        // Simulated API call to get mock information for riders
        try {
          const results = await new Promise((resolve) => {
            setTimeout(() => {
              const generatedData = [];
              for (let i = 0; i < numberOfRiders; i++) {
                generatedData.push({
                  "Rider number": { value: `L${i + 1}`, confidence: 0.8 + Math.random() * 0.2 },
                  "Recovery": { value: Math.floor(Math.random() * 10), confidence: 0.5 + Math.random() * 0.5 },
                  "Hydration": { value: Math.floor(Math.random() * 10), confidence: 0.5 + Math.random() * 0.5 },
                  "Lesions": { value: Math.floor(Math.random() * 10), confidence: 0.5 + Math.random() * 0.5 },
                  "Soundness": { value: Math.floor(Math.random() * 10), confidence: 0.5 + Math.random() * 0.5 },
                  "Qual Mvmt": { value: Math.floor(Math.random() * 10), confidence: 0.5 + Math.random() * 0.5 },
                  "Ride time, this rider": { value: 300 + Math.floor(Math.random() * 100), confidence: 0.8 + Math.random() * 0.2 },
                  "Weight of this rider": { value: 150 + Math.floor(Math.random() * 50), confidence: 0.7 + Math.random() * 0.3 },
                });
              }
              resolve(generatedData);
            }, 100);
          });

          console.log('Image processed successfully:', results);

          // Store the extracted data for all riders
          setExtractedDataList(results);
          setCurrentStep(3); // Proceed to show extracted data

        } catch (error) {
          console.error('Error uploading image:', error);
        }
      }
    } else {
      console.error("No image to upload.");
    }
  };

  const handleGoBackToUpload = () => {
    setCurrentStep(1);
    setImageSrc1(null);
    setImageSrc2(null);
    setImageFile1(null);
    setImageFile2(null);
  };

  return (
    <div className="App">
      {currentStep === 3 ? (
        // If we have extracted data for all riders, show the BCEExtractedValues component for each rider
        <div className="bce-results-container">
          <BCEExtractedValues
            extractedDataList={extractedDataList}
            onGoBackToUpload={handleGoBackToUpload}
            heaviestRiderWeight={heaviestRiderWeight}
            fastestRiderTime={fastestRiderTime}
            numberOfRiders={numberOfRiders}
          />
        </div>
      ) : (
        <>
          {/* Display upload section for photos */}
          {((currentStep === 1 && !imageSrc1) || (isTwoPhotosRequired && currentStep === 2 && !imageSrc2)) ? (
            <div className="button-container">
              <h2>
                {currentStep === 1 ? `Select Scorecard 1` : `Select Scorecard 2`}
              </h2>
              <input
                type="file"
                accept="image/*"
                capture="environment"
                ref={fileInputRef}
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
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
              <img src={currentStep === 1 ? imageSrc1 : imageSrc2} alt="Preview" className="image-fullscreen" />
              {/* Buttons for retaking or continuing */}
              <div className="action-buttons">
                <button className="scorecard-button" onClick={handleRetakePhoto}>
                  Retake Image
                </button>
                <button className="scorecard-button" onClick={handleContinue}>
                  {isTwoPhotosRequired && currentStep === 1 ? "Continue to Scorecard 2" : "Continue"}
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default GetPhotoBCE;
