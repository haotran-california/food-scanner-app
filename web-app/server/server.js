const express = require('express') 
const cors = require('cors') 

const app = express()
const port = process.env.PORT || 6002

const URL = `http://localhost:${port}`
const clientID = ''
const clientSECRET = ''
const callbackURL = URL

app.use(cors())
app.use(express.json())

app.get('/', async (req, res) => {

	res.send('hello world') 
})

app.listen(port, () => {
	console.log(`Listening on port ${port}...`) 
})

