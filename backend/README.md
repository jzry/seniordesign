# Express.js server

The primary functionality of the backend of this application is to retrieve image data from the frontend, send the image to the OCR, run the OCR with the image, get the results of the OCR in JSON-encoded form, and send the JSON-encoded data to be parsed and displayed by the frontend.

NOTE: You currently may not change the port number but I'm working on that.

## Run in development mode

### Change environment variable(s)

In the main project directory, navigate to `process.env`. Set `MODE=development` to enable dev mode, if it's not already enabled. In `process.env`, you should also see `PORT=8080`. <!-- If port 8080 is currently busy, you may change it as needed. -->

### Node module installation

Enter `npm i` terminal within the backend directory to download requisite node modules

### To run

This application is run by entering `node server.js` in the terminal within the backend directory

### Standalone test

Once running, navigate to `http://localhost:8080/` in your web browser. <!-- If you changed your port number, simply replace `8080` with your chosen port -->. If successful, you should see a message reading "Hello from our server!"

### Test with frontend

While running the application, open up a new terminal window, navigate to the frontend directory, and enter `npm run start` to start up the React app on `http://localhost:3000/`. You may now use the app while it's in development.

## Create a production build

### Change environment variable(s)

In the `process.env` file in the main project directory, set `MODE=production` if it isn't already. <!-- You may also change the port number as needed. -->

### Build React app

Navigate to the frontend directory in a terminal window. Enter the command `npm run build`, which compiles the frontend of the application such that it may be served statically, rather than as a standalone application.

### Run the application

Navigate to the backend directory in a terminal window. Enter the command `node server.js` to launch the application. In you browser, navigate to `http://localhost:8080/`. <!-- If you changed your port number, simply replace `8080` with your chosen port. --> You should now be able to use the application.

## Use PM2 process manager (optional unless deploying)

Please note that the following instructions are completely optional for basic testing unless you are deploying to the web server and will probably only work if you are using a Linux distro/WSL (I haven't tested it with Windows since virtually all web servers use Linux)

### Download PM2

In a terminal window, enter the command `npm install -g pm2` to install PM2 globally. If you are denied permission, prepend `sudo` to the command and you will be asked for your Linux password.

### Launch and Daemonize the Node app

Navigate to the backend directory and enter `pm2 start server.js` to launch the PM2 instance of the Express app. Now, in your web browser, you may access the app from localhost without needing to launch it in Node first

### Update PM2 instance

If you make changes to the application, enter `pm2 reload server.js`.

### Delete PM2 instance

If you wish to delete the PM2 instance, enter `pm2 delete server.js`.
