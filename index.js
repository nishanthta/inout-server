const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors');
const { getDatabase } = require("./database")
const app = express()
const port = 5000

app.use(bodyParser.json())
app.use(cors())

getDatabase()
    .then(db => {
        app.get('/', (req, res) => res.send('Hello World!'))

        app.post('/sign-up-advertiser', async (req, res) => {
            const advertisers = db.collection('advertisers');
            try {
                await advertisers.insertOne(req.body);
                res.sendStatus(200);
            } catch (err) {
                res.send(err);
            }
        });

        app.listen(port, () => console.log(`Bubblegum running at port ${port}!`))
    });