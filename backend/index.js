const express = require('express');
const fileUpload = require('express-fileupload')
const cors = require('cors');
const path = require('path')

// Get the fake API data simulating the affects of the OCR
const fakeData = require('./fakeAPIData/fake-ctr-json.json')

// The express app
const app = express();

// Allow cross-origin resource sharing
app.use(cors())

// Use express-fileupload
app.use(fileUpload())

// Basic t
app.get('/', (req, res) => {
    res.send('Hello from our server!')
})

app.get('/ctr', (req, res) => {
  res.json(fakeData)
})

// Retrieve the uploaded image from the handleSubmit function in frontend/src/pages/crt/getPhotos.js
app.post('/upload', (req, res) => {
    console.log('Upload endpoint hit');  // Log this to see if request is received

    let sampleFile;
    let uploadPath;
  
    if (!req.files || Object.keys(req.files).length === 0) {
      return res.status(400).send('No files were uploaded.');
    }
  
    // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
    sampleFile = req.files.image;
    // uploadPath = path.join(__dirname, '/imgs/', sampleFile.name) 
    uploadPath = path.join(__dirname, '../Uploads/test.jpg') 
  

    console.log('File received:', sampleFile.name);  // Log file details

    // Use the mv() method to place the file somewhere on your server
    sampleFile.mv(uploadPath, function(err) {
      if (err)
        return res.status(500).send(err);
  
      res.send('File uploaded!');
    });
  });


module.exports = app

