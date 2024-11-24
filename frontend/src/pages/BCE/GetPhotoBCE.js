import React, { useState, useRef } from 'react';
import UploadIcon from "../../images/upload.png";
import BCEExtractedValues from './BCEExtractedValues';
import '../../styles/CTRHandWritingRecognitionStyles.css';
import axios from 'axios';

// GetPhotoBCE Component: Handles image uploads and sends data to the backend
function GetPhotoBCE({ numberOfRiders, fastestRiderTime, heaviestRiderWeight }) {
  const [imageSrc1, setImageSrc1] = useState(null);
  const [imageSrc2, setImageSrc2] = useState(null);
  const [imageFile1, setImageFile1] = useState(null);
  const [imageFile2, setImageFile2] = useState(null);
  const [extractedDataList, setExtractedDataList] = useState([]);
  const [currentStep, setCurrentStep] = useState(1);
  const fileInputRef = useRef(null);
  const apiUrl = process.env.REACT_APP_API_URL


  const isTwoPhotosRequired = numberOfRiders > 5;

  // Handles file selection for images
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

  // Submits selected images to the backend
  const handleSubmit = async (event) => {
    event.preventDefault()

    const formData = new FormData()

    if (imageFile1 && !imageFile2) {
      formData.append('image', imageFile1)
    } else if (imageFile2) {
      formData.append('image', imageFile2);
    }
    else {
        console.error('No images available to submit')
        return
    }

    axios.post(apiUrl.concat('/bce'), formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(response => {
      if (response.data.error) {
        console.error("The image was not processed correctly")
      }


      let bceData = extractedDataList

      Object.keys(response.data).forEach(key => {
        if (bceData.length < numberOfRiders) {
            bceData.push(response.data[key])
        }
      })

      setExtractedDataList(bceData)
      console.log("Data Retrieved:")
      console.log(bceData)

      if (!isTwoPhotosRequired && currentStep === 1) {
        setCurrentStep(3)
      }
    })
    .catch(error => {
        console.error('Error uploading file:', error);
    })
  };

  // Retakes the current photo
  const handleRetakePhoto = () => {
    if (currentStep === 1) {
      setImageSrc1(null);
      setImageFile1(null);
    } else {
      setImageSrc2(null);
      setImageFile2(null);
    }
  };

  // Go to the next step or the next photo
  const handleContinue = async () => {
    if (isTwoPhotosRequired && currentStep === 1) {
      // Move to step 2 to capture the second photo for the current group
      setCurrentStep(2)
    } else if (currentStep === 2){
      setCurrentStep(3)
    }

    console.log(currentStep)
  };

  // Returns to the upload step
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
                <button className="scorecard-button" onClick={(event) => { handleSubmit(event); handleContinue() }}>
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
