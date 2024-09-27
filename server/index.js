const express = require('express')
const cors = require('cors')
const app = express();

app.use(cors())

app.get('/', (req, res) => {
    res.json({success: true})
})

app.listen(8080, () => {
    console.log('server listening on port 8080')
})