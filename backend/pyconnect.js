const { spawn } = require('child_process');


//
// Send an image to the BCE Python script
//
// Returns a promise!!! 'await' a JSON object
//
exports.processBCE = function (image) {

    return runScript('scanBCE.py', image)
}

//
// Send an image to the CTR Python script
//
// Returns a promise!!! 'await' a JSON object
//
exports.processCTR = function (image) {

    return runScript('scanCTR.py', image)
}


//
// Handles the creation of the child process in which Python runs
//
function runPythonProcess(scriptName, image)
{
    return new Promise((accept, reject) => {

        // Create the process. Pass the script name and the number of bytes as command line arguments
        //
        const pythonProcess = spawn('python', [scriptName, image.size])

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
async function runScript(scriptName, image)
{
    try
    {
        var res = await runPythonProcess(scriptName, image)
    }
    catch (e)
    {
        console.error(e)
        return {
            error: 'The child process has encountered an error',
            status: 500
        }
    }

    try
    {
        var ret = JSON.parse(res)

        if (ret.status)
        {
            if (ret.status >= 500)
                console.error(ret.error)
            else
                console.warn(ret.error)
        }
    }
    catch (e)
    {
        console.error(`ERROR (${__filename}): ${e.message}\n${res}`)
        var ret = {
            error: 'The child process returned a corrupted value',
            status: 500
        }
    }

    return ret
}

