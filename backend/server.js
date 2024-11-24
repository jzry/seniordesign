const app = require('./index')
require('dotenv').config({ path: '../process.env' });


const port = process.env.PORT


// 8080 is the port we are using in the meantime, but may be changed later (probably)
app.listen(port, () => {
    console.log('server listening on port ' + port)
})
