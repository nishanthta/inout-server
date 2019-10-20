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

        app.post('/sign-up-developer', async (req, res) => {
            const developers = db.collection('developers');
            try {
                await developers.insertOne(req.body);
                res.sendStatus(200);
            } catch (err) {
                res.send(err);
            }
        });

        app.get('/get-ad-proposals', async(req, res) => {
            const pc = db.collection('proposals');
            const appId = req.query.appId;
            console.log(appId);
            try {
                let proposals = await pc.find({ appId: appId }).toArray();
                proposals = sorter(proposals, 'offerValue');
                res.send(proposals);
            } catch (err) {
                console.error(err);
                res.sendStatus(500);
            }
        });

        app.get('/get-dev-requests', async(req, res) => {
            const pc = db.collection('dev-requests');
            const email = req.query.email;
            console.log(email);
            try {
                let proposals = await pc.find({ email: email }).toArray();
                res.send(proposals);
            } catch (err) {
                console.error(err);
                res.sendStatus(500);
            }
        });

        app.get('submit-dev-request', async(req, res) => {
            const app = req.body;
            const pc = db.collection('dev-requests');
            const email = app.email;
            console.log(email);
            const p = await pc.find({ email }).toArray();
            for (const a of p) {
                if (a.appId === app.appId) {
                    res.sendStatus(403);
                    return;
                }
            }
            try {
                await pc.insertOne(app);
                res.sendStatus(200);
            } catch (err) {
                console.error(err);
                res.sendStatus(500);
            }
        })

        app.post('/submit-ad-proposal', async (req, res) => {
            const proposal = req.body;
            const pc = db.collection('proposals');
            const p = await pc.find({ appId: req.body.appId }).toArray();
            for (const ad of p) {
                if (ad.email == proposal.email) {
                    res.sendStatus(403);
                    return;
                }
            }
            try {
                await pc.insertOne(proposal);
                res.sendStatus(200);
            } catch (err) {
                res.send(err);
            }
        });

        app.listen(port, () => console.log(`Bubblegum running at port ${port}!`))
    });