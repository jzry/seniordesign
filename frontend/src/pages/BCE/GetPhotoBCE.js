import React, { useState, useRef, useEffect } from 'react';
import UploadIcon from "../../images/upload.png";
import BCEExtractedValues from './BCEExtractedValues';
import '../../styles/CTRHandWritingRecognitionStyles.css';
import axios from 'axios';

function GetPhotoBCE({ numberOfRiders, fastestRiderTime, heaviestRiderWeight }) {
  const [imageSrc, setImageSrc] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [extractedDataList, setExtractedDataList] = useState([]);
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [backendError, setBackendError] = useState(null);
  const canvasRef = useRef(null);
  const apiUrl = process.env.REACT_APP_API_URL;

  const [corners, setCorners] = useState([
    { x: 100, y: 100 },
    { x: 300, y: 100 },
    { x: 300, y: 300 },
    { x: 100, y: 300 }
  ]);
  const [draggingCorner, setDraggingCorner] = useState(null);
  const [isCropping, setIsCropping] = useState(false);

  const isTwoPhotosRequired = numberOfRiders > 5;

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setImageSrc(imageUrl);
      setImageFile(file);
      setIsCropping(true);
    }
  };

  const handleMouseDown = (event) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    const cornerIndex = corners.findIndex(corner => 
      Math.hypot(corner.x - x, corner.y - y) < 10
    );

    if (cornerIndex !== -1) {
      setDraggingCorner(cornerIndex);
    }
  };

  const handleMouseMove = (event) => {
    if (draggingCorner !== null) {
      const rect = canvasRef.current.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      setCorners(prevCorners => {
        const updatedCorners = [...prevCorners];
        updatedCorners[draggingCorner] = { x, y };
        return updatedCorners;
      });
    }
  };

  const handleMouseUp = () => {
    setDraggingCorner(null);
  };

  const handleContinue = () => {
    setIsCropping(false);
  };

  const cropAndSubmit = async () => {
    setLoading(true);
    setBackendError(null);

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const image = new Image();
    image.src = imageSrc;

    image.onload = async () => {
      const xMin = Math.min(...corners.map(c => c.x));
      const yMin = Math.min(...corners.map(c => c.y));
      const xMax = Math.max(...corners.map(c => c.x));
      const yMax = Math.max(...corners.map(c => c.y));

      const croppedWidth = xMax - xMin;
      const croppedHeight = yMax - yMin;

      const croppedCanvas = document.createElement("canvas");
      const croppedCtx = croppedCanvas.getContext("2d");
      croppedCanvas.width = croppedWidth;
      croppedCanvas.height = croppedHeight;

      croppedCtx.drawImage(image, xMin, yMin, croppedWidth, croppedHeight, 0, 0, croppedWidth, croppedHeight);

      croppedCanvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('image', blob, 'cropped_image.png');

        try {
          const response = await axios.post(apiUrl.concat('/bce'), formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });

          if (response.data.error) {
            throw new Error(response.data.error);
          }

          let bceData = [...extractedDataList];
          response.data.riderData.forEach((rider) => {
            if (bceData.length < numberOfRiders) {
              bceData.push(rider);
            }
          });

          setExtractedDataList(bceData);
          setCurrentStep(3);
        } catch (error) {
          setBackendError(error.message || "An unknown error occurred.");
        } finally {
          setLoading(false);
        }
      });
    };
  };

  useEffect(() => {
    if (imageSrc && isCropping) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      const image = new Image();
      image.src = imageSrc;

      image.onload = () => {
        canvas.width = image.width;
        canvas.height = image.height;
        ctx.drawImage(image, 0, 0);

        ctx.strokeStyle = "red";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(corners[0].x, corners[0].y);
        for (let i = 1; i < corners.length; i++) {
          ctx.lineTo(corners[i].x, corners[i].y);
        }
        ctx.closePath();
        ctx.stroke();

        ctx.fillStyle = "blue";
        corners.forEach((corner) => {
          ctx.beginPath();
          ctx.arc(corner.x, corner.y, 5, 0, 2 * Math.PI);
          ctx.fill();
        });
      };
    }
  }, [imageSrc, corners, isCropping]);

  return (
    <div className="App">
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
        </div>
      )}
      {currentStep === 3 ? (
        <div className="bce-results-container">
          <BCEExtractedValues
            extractedDataList={extractedDataList}
            onGoBackToUpload={() => setCurrentStep(1)}
            heaviestRiderWeight={heaviestRiderWeight}
            fastestRiderTime={fastestRiderTime}
            numberOfRiders={numberOfRiders}
          />
        </div>
      ) : (
        <>
          {!imageSrc ? (
            <div className="button-container">
              <h2>Select Scorecard</h2>
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
            <>
              {isCropping ? (
                <div className="canvas-container">
                  <canvas
                    ref={canvasRef}
                    onMouseDown={handleMouseDown}
                    onMouseMove={handleMouseMove}
                    onMouseUp={handleMouseUp}
                  />
                  <button className="scorecard-button" onClick={handleContinue}>
                    Continue with Cropped Image
                  </button>
                </div>
              ) : (
                <div className="image-fullscreen-container">
                  <img src={imageSrc} alt="Preview" className="image-fullscreen" />
                  <div className="action-buttons">
                    <button className="scorecard-button" onClick={cropAndSubmit}>
                      Submit Cropped Image
                    </button>
                  </div>
                </div>
              )}
            </>
          )}
          {backendError && <div className="error-message">{backendError}</div>}
        </>
      )}
    </div>
  );
}

export default GetPhotoBCE;
