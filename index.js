const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors');
const { getDatabase } = require("./database")
const sorter = require("./sorter");
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

        app.get('/get-ad-proposals', async(req, res) => {
            const pc = db.collection('proposals');
            try {
                let proposals = await pc.find({}).toArray();
                proposals = sorter(proposals, 'offerValue');
                res.send(proposals);
            } catch (err) {
                console.error(err);
                res.sendStatus(500);
            }
        });

        app.post('/submit-ad-proposal', async (req, res) => {
            const proposal = req.body;
            const pc = db.collection('proposals');
            try {
                await pc.insertOne(proposal);
                res.sendStatus(200);
            } catch (err) {
                res.send(err);
            }
        });

        app.listen(port, () => console.log(`Bubblegum running at port ${port}!`))
    });