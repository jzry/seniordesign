const express = require('express');
const fileUpload = require('express-fileupload')
const cors = require('cors');
const path = require('path')
const app = express();

app.use(cors())
app.use(fileUpload())

app.get('/', (req, res) => {
    res.send('Hello from our server!')
})

app.get('/test', (req, res) => {
    console.log('Test route hit');
    res.send('Test route works!');
  });

app.post('/upload', function(req, res) {
    console.log('Upload endpoint hit');  // Log this to see if request is received

    let sampleFile;
    let uploadPath;
  
    if (!req.files || Object.keys(req.files).length === 0) {
      return res.status(400).send('No files were uploaded.');
    }
  
    // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
    sampleFile = req.files.image;
    uploadPath = path.join(__dirname, '/imgs/', sampleFile.name) 
  

    console.log('File received:', sampleFile.name);  // Log file details

    // Use the mv() method to place the file somewhere on your server
    sampleFile.mv(uploadPath, function(err) {
      if (err)
        return res.status(500).send(err);
  
      res.send('File uploaded!');
    });
  });


app.listen(8080, () => {
    console.log('server listening on port 8080')
})
