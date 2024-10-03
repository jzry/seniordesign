import React, { useState, useRef } from 'react';
import CameraIcon from "../images/camera.png";
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

  return (
    <div className="App">
      <div className="button-container">
        {/* Hidden file input to trigger the camera */}
        <input
          type="file"
          accept="image/*" // Restrict to image files and trigger camera on mobile devices
          capture="environment" // Use the back camera if available
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

      {/* Display the captured or uploaded image */}
      {imageSrc && (
        <div className="image-preview">
          <img src={imageSrc} alt="Preview" />
        </div>
      )}
    </div>
  );
}

export default GetPhotos;
