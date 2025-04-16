# Environment Variable Reference

A comprehensive list of all environment variables that are used by this web app.
Not all of these are required to be set for development. The variables that must be set
in order to run will be labeled :exclamation:***Required***.

## :page_facing_up: File: `backend/.env`

### PORT

:exclamation:***Required***

The port number that the Express server will communicate on.
Ports `80`, `8008`, and `8080` are typically used for HTTP. Port `443` is used for HTTPS.
For testing on localhost, you can use any port not being used by your computer.
For a list of commonly used ports see
[this wikipedia page](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers).

### MODE

:exclamation:***Required***

This can be set to either `development` or `production`.
If `production` is specified, the React frontend will be
served statically from Express (Remember to run the frontend build script first!).

### NODE_ENV

This can be set to either `development` or `production`.
This value will determine if node.js will run in development or
production mode.

### PYTHON_CMD

Sets the string used to run Python. Depending on your system and configuration this could be
`python3`, `python`, or `py`. By default, `python3` is used.

### PROTOCOL

This can be either `http` or `https`. The default value is `http`. If `https` is specified,
a second Express server will be created using HTTP on port 80 that redirects traffic to the HTTPS
server.

### KEY_FILE

:exclamation:***Required if PROTOCOL is set to `https`***

The path to a file containing the private key of the SSL certificate.

### CERT_FILE

:exclamation:***Required if PROTOCOL is set to `https`***

The path to a file containing the server certificate of the SSL certificate.

### ORIGIN

The origin to use for CORS security. CORS will block requests that come from origins other
than the one specified here. For example, this might be set to `https://stirup.co`.
If this variable is ommitted, then CORS will allow requests from any origin (`*`).

### LITSERVE_PORT

The port number that the model server will run on. By default, it will run on
port `8000`.

### LITSERVE_URL

If LitServe is to be run on a seperate server, you can specify the url to
access it.

### LIT_SERVER_API_KEY

Sets the LitServe authentication key. All requests must contain this key in the
`X-API-Key` header. If this variable is ommitted, all requests will be accepted
without authentication.

### BYPASS_LITSERVE

LitServe is used by default. By setting this variable to any value, the OCR
will not use LitServe and directly load the image classifier model instead.

## :page_facing_up: File: `frontend/.env`

> [!IMPORTANT]
> These variables should be up to date before performing a static build.
> If any changes are made to this file after a build, you must rebuild to use the
> latest values.

### REACT_APP_API_URL

:exclamation:***Required***

The base url for calling api endpoints. For example, `http://localhost:8080` would be
the correct url if the express server is running on port 8080 of your computer. If you would
like to test the website on devices on your local network, replace localhost with the ip address
of your computer.

