const { spawn } = require('child_process');


// The command to run Python
const pythonCommand = (process.env.PYTHON_CMD) ? process.env.PYTHON_CMD : 'python3'

// A string that determines if TorchServe is used or not
const torchserveParam = (process.env.TORCHSERVE) ? process.env.TORCHSERVE.toLowerCase() : 'no_torchserve'

// The default error response if something goes wrong
const defaultErrorResponse = { body: { error: 'An error occured while processing your request' }, status: 500 }


//
// Send a BCE image to the Python script
//
// Returns a promise!!! 'await' a JSON object
//
exports.processBCE = function (image) {

    return runScript('bce', image)
}

//
// Send a CTR image to the Python script
//
// Returns a promise!!! 'await' a JSON object
//
exports.processCTR = function (image) {

    return runScript('ctr', image)
}


//
// Handles the creation of the child process in which Python runs
//
function runPythonProcess(imageType, image)
{
    return new Promise((accept, reject) => {

        // Create the process. Pass the script name and the number of bytes as command line arguments
        //
        const pythonProcess = spawn(pythonCommand, ['jsconnect.py', image.size, imageType, torchserveParam])

        let result = ''
        let errResult = ''

        // Catch general errors
        //
        pythonProcess.on('error', (err) => {

            reject(err)
        })

        // Write the image data to the process's stdin buffer
        //
        if (pythonProcess.stdin)
        {
            pythonProcess.stdin.write(image.data)

            pythonProcess.stdin.on('error', (err) => {

                console.warn(`(${__filename}) ${err}`)
            })
        }

        // Read response data
        //
        pythonProcess.stdout.on('data', (data) => {

            result += data
        })

        // Read error data
        //
        pythonProcess.stderr.on('data', (data) => {

            errResult += data
        })

        // The program is done. Return the results
        //
        pythonProcess.stdout.on('end', () => {

            if (errResult)
            {
                reject(errResult)
            }
            else
            {
                accept(result)
            }
        })
    })
}


//
// Calls the process creation function and parses its outputs
//
async function runScript(imageType, image)
{
    try
    {
        // Run Python code
        var output = await runPythonProcess(imageType, image)
    }
    catch (e)
    {
        var output = { error: e.message, status: -1 }
    }

    try
    {
        // Parse output string as JSON
        var json = JSON.parse(output)
    }
    catch (e)
    {
        var json = { error: e.message, status: -2 }
    }

    // Reformat the JSON before returning it
    return processReturnValue(json)
}


//
// Processes the Python output into a format ready to be returned by the API,
// and logs any error messages.
//
// (Returns) A JSON object of the form:
//
//     { "body": <the response body>, "status": <the repsonse status code> }
//
function processReturnValue(val)
{
    if (typeof val.status === 'undefined' || val.status < 0)
    {
        if (val.error)
        {
            console.error(val.error)
        }

        return defaultErrorResponse
    }

    if (val.status === 0)
    {
        if (!val.data)
        {
            console.error('"data" field missing from Python response')
            return defaultErrorResponse
        }

        return { body: val.data, status: 200 }
    }

    //if (val.status === 1)
    //{
    //    console.warn('')
    //}

    console.error(`Unrecognized or invalid value for Python return status: ${val.status}`)
    return defaultErrorResponse
}

