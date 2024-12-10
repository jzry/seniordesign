//
// A Github hook endpoint for automatically
// updating the server with the latest code.
//

const express = require('express')
const { spawn } = require('child_process')
const validateHook = require('./hookValidation')

const router = express.Router()
router.use(express.json())

let updateFlag = false


router.post('/update', async (req, res) => {

    // Authenticate this request before acting on it
    let authHeader = req.headers['x-hub-signature-256']
    let valid = await validateHook(process.env.GITHUB_SECRET, authHeader, JSON.stringify(req.body))

    if (valid)
    {
        // Perform an update when a pull request is merged
        let pull_request_merged = req.body.action === 'closed' &&
                                  req.body.pull_request &&
                                  req.body.pull_request.merged

        if (pull_request_merged)
        {
            // If the update flag is already set,
            // an update is currently in progress.
            if (!updateFlag)
            {
                updateFlag = true

                console.log(`${req.connection.remoteAddress}\t| ${req.url}\t| Update request accepted`)

                // Launch a bash script to perform the update
                const updateScript = spawn('./updateScript')

                updateScript.on('error', err => {

                    console.error(`${req.connection.remoteAddress}\t| ${req.url}\t| Update request failed`)
                    updateFlag = false
                })

                updateScript.on('close', code => {

                    if (code !== 0)
                    {
                        console.error(`${req.connection.remoteAddress}\t| ${req.url}\t| Update request failed`)
                        updateFlag = false
                    }
                })
            }
            else
            {
                console.warn(`${req.connection.remoteAddress}\t| ${req.url}\t| Update already in progress`)
                res.status(429)
            }
        }
        else
        {
            console.log(`${req.connection.remoteAddress}\t| ${req.url}\t| Update request ignored`)
        }

        res.send('Request received')
    }
    else
    {
        res.status(401).send('Failed to authenticate the request')
        console.warn(`${req.connection.remoteAddress}\t| ${req.url}\t| Failed to authenticate`)
    }
})


module.exports = router
