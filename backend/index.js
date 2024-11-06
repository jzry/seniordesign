const express = require('express');
const fileUpload = require('express-fileupload')
const cors = require('cors');
const cookieParser = require('cookie-parser')
const path = require('path')
const pyconnect = require('./pyconnect')


// Get the fake API data simulating the affects of the OCR
const fakeCTRData = require('./API-Tests/fake-ctr-json.json')
const fakeBCEData = require('./API-Tests/fake-bce-json.json')

// Request validation middleware for the CTR data from the OCR
// Because the CTR data is not currently sourced from an api endpoint, this function only simulates the functionality of Express Middleware
function validateData(/*req, res, next*/ fakeCTRData) {
  let req = { body: fakeCTRData }
  if (typeof req.body !== 'object' || req.body === null) {
    return res.status(400).json({ error: 'Invalid JSON object in request body.' });
  }

  for (const key in req.body) {
    const item = req.body[key];

    // Check if item is an object with "value" and "confidence" keys
    if (
      typeof item !== 'object' ||
      item === null ||
      !('value' in item) ||
      !('confidence' in item)
    ) {
      return res.status(400).json({ error: `Invalid format for key "${key}". Each value should contain "value" and "confidence" fields.` });
    }

    // Validate that the request 
    if (!Number.isInteger(item.value)) {
      return res.status(400).json({ error: `Invalid value for "${key}". "value" must be an integer.` });
    }
    if (typeof item.confidence !== 'number' || item.confidence < 0 || item.confidence > 1) {
      return res.status(400).json({ error: `Invalid confidence for "${key}". "confidence" must be a float between 0 and 1.` });
    }
  }

  return

  // If all validations pass, proceed
  // next();
}

// Middleware function to validate the image input by the user
function validateImage(req, res, next) {
  const allowedFileTypes = ['image/jpeg', 'image/png'];
  const maxSize = 5 * 1024 * 1024; // 5 MB limit

  // Check if file exists
  if (!req.files || !req.files.image) {
    console.log('No file uploaded.')
    return res.status(400).send('No file uploaded.');
  }

  const image = req.files.image;

  // Check file size
  if (image.size > maxSize) {
    console.log('File size exceeds limit of 5 MB.')
    return res.status(400).send('File size exceeds limit of 5 MB.');
  }

  // Check file type
  if (!allowedFileTypes.includes(image.mimetype)) {
    console.log('Invalid file type. Only JPEG, PNG allowed.')
    return res.status(400).send('Invalid file type. Only JPEG, PNG allowed.');
  }

  // If all checks pass, proceed
  next();
}

// Cross-Origin Resource Sharing Middleware to only accept data originating from our frontend
const corsOptions = {
  origin: /^http:\/\/localhost:3000(\/.*)?$/,
  optionsSuccessStatus: 200,
};


// The express app
const app = express();

// Allow cross-origin resource sharing
app.use(cors(corsOptions))

// Use cookie parser
app.use(cookieParser())

// Use express-fileupload
app.use(fileUpload())



app.get('/', (req, res) => {
  res.send('Hello from our server!')
})

app.get('/ctr', (req, res) => {
  /*validateData*/
  res.json(fakeCTRData)
})

app.get('/bce', (req, res) => {
  /*validateData*/
  res.json(fakeBCEData)
})

// Retrieve the uploaded image from the handleSubmit function in frontend/src/pages/crt/getPhotos.js

app.post('/uploadCTR', validateImage, (req, res) => {
  console.log('CTR Upload endpoint hit');  // Log this to see if request is received

  let sampleFile;
  let uploadPath;

  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }

  // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
  sampleFile = req.files.image;
  // uploadPath = path.join(__dirname, '/imgs/', sampleFile.name) 
  uploadPath = path.join(__dirname, '../Uploads/testCTR.jpg')

  console.log('File received:', sampleFile.name);  // Log file details

  // Use the mv() method to place the file somewhere on your server
  sampleFile.mv(uploadPath, function (err) {
    if (err)
      return res.status(500).send(err);

    res.send('File uploaded!');
  });
});

app.post('/uploadBCE', validateImage, (req, res) => {
  console.log('BCE Upload endpoint hit');  // Log this to see if request is received

  let sampleFile;
  let uploadPath;

  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }

  // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
  sampleFile = req.files.image;
  // uploadPath = path.join(__dirname, '/imgs/', sampleFile.name) 
  uploadPath = path.join(__dirname, '../Uploads/testBCE.jpg')

  console.log('File received:', sampleFile.name);  // Log file details

  // Send the image to the Python code to be processed
  output = await pyconnect.processBCE(sampleFile)

  if (output.error)
    res.status(500)

  res.json(output)
});


module.exports = app
// app.listen(8080, () => {
//   console.log('server listening on port 8080')
// })