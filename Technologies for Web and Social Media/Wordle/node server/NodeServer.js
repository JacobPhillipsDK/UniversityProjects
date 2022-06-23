const express = require('express');
const app = require('express')() // Initialize the app
const port = 3000
const path = require('path');
const {MongoClient} = require('mongodb'); // var MongoClient = require('mongodb').MongoClient;

DEBUG = false;
let wordlist = [];


function getRandomNumber(min, max) {
    return wordlist[Math.floor(Math.random() * (max - min + 1)) + min]
}


app.post('/', (req, res) => {
    res.send('Got a POST request')
    console.log(req.body)
})


async function main() {
    /**
     * Connection URI. Update <username>, <password>, and <your-cluster-url> to reflect your cluster.
     * See https://docs.mongodb.com/ecosystem/drivers/node/ for more details
     */
    const uri = "mongodb+srv://WordlePlayer:Play123@worldecluster.ktr3j.mongodb.net/WorldeCluster?retryWrites=true&w=majority";
    const client = new MongoClient(uri);


    async function listDatabases(client) {
        let databasesList = await client.db().admin().listDatabases();
        if (DEBUG) {
            console.log("Databases:");
            databasesList.databases.forEach(db => console.log(` - ${db.name}`));
        }

    }

    try {
        const database = client.db("WordsForGame");
        const Words = database.collection("Words");


        // specify the document field
        const fieldName = "word";
        // specify an optional query document

        await client.connect();
        console.log("Connected to database Successfully");

        const estimate = await Words.estimatedDocumentCount();
        const distinctValues = await Words.distinct(fieldName);


        for (let i = 0; i < distinctValues.length; i++) {
            wordlist.push(distinctValues[i])
        }
        console.log("Random Word is :" + getRandomNumber(0, wordlist.length), "wordlist.length : " + wordlist.length);
        if (DEBUG) {
            console.log("wordlist: ", wordlist.length)
            console.log("The Random Word from the DataBase is: ", wordlist[Math.floor(Math.random() * (wordlist.length + 1))])
            console.log(`Estimated number of documents in the movies collection: ${estimate}`);
            // console.log("distinctValues" + distinctValues);
        }

        // Make the appropriate DB calls
        await listDatabases(client);

    } catch (e) {
        console.error(e);
    } finally {
        await client.close();
    }
}

main().catch(console.error);


app.use(express.static(path.join(__dirname, 'public'))); // Gets the static files such as HTML, CSS, JS, Images

app.get('/', (req, res) => { //
    // Telling hte express module that the public dir has all of our sites assets
    res.sendFile(__dirname + '/index.html'); // Sending the index.html file to the client
    console.log("req.url  & req.method" + req.url + " " + req.method);
    res.json({
        "word": getRandomNumber(0, wordlist.length)
    });
})

// Req = Incoming data request from client side
// Res = Outgoing data response to client side
app.get('/getword',(req,res) => {
    res.status(200).send({
        "word": getRandomNumber(0, wordlist.length)
    })
    console.log("User Send request for new word");
});


app.listen(port, () => {
    console.log(`App is alive and listening at http://localhost:${port}`)
})