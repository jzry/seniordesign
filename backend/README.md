# Express.js server

The primary functionality of the backend of this application is to retrieve image data from the frontend, send the image to the OCR, run the OCR with the image, get the results of the OCR in JSON-encoded form, and send the JSON-encoded data to be parsed and displayed by the frontend.

## To run

### Node module installation

Enter `npm i` terminal within the backend directory to download requisite node modules

### To run

This application is run by entering `node index.js` in the terminal within the backend directory

### Standalone test

Once running, navigate to "http://localhost:8080/" in your web browser. If successful, you should see a message reading "Hello from our server!"

### Test with frontend

While running the application, open up a new terminal window, navigate to the frontend directory, and enter `npm run start` to start up the React app on "http://localhost:3000/". If you navigate to the CTR Scorecard and submit an uploaded image, this image should be sent to the "Image Processing Test"