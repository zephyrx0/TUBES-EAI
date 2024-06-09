const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(bodyParser.json());

const uri = 'mongodb+srv://ganelajeisa:ganelajeisa@cluster0.4ula36n.mongodb.net/obat';
let obatCollection;

// Connect to MongoDB
MongoClient.connect(uri, { useUnifiedTopology: true })
    .then(client => {
        const db = client.db('obat');
        obatCollection = db.collection('obat');
        console.log('Connected to Database');
    })
    .catch(error => console.error(error));

// Endpoint untuk mendapatkan data obat
app.get('/obat', (req, res) => {
    obatCollection.find({}, { projection: { _id: 0 } }).toArray()
        .then(results => {
            res.status(200).json(results);
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk menambah data obat
app.post('/obat', (req, res) => {
    const data = req.body;
    obatCollection.insertOne(data)
        .then(result => {
            res.status(201).json(result.ops[0]);
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk menghapus data obat berdasarkan ID
app.delete('/obat/:id', (req, res) => {
    const id = req.params.id;
    obatCollection.deleteOne({ _id: new ObjectId(id) })
        .then(result => {
            if (result.deletedCount > 0) {
                res.status(200).json({ message: 'Obat deleted' });
            } else {
                res.status(404).json({ error: 'Obat not found' });
            }
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk mengupdate data obat berdasarkan ID
app.put('/obat/:id', (req, res) => {
    const id = req.params.id;
    const data = req.body;
    obatCollection.updateOne(
        { _id: new ObjectId(id) },
        { $set: data }
    )
        .then(result => {
            if (result.matchedCount > 0) {
                res.status(200).json({ message: 'Obat updated' });
            } else {
                res.status(404).json({ error: 'Obat not found' });
            }
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

const PORT = process.env.PORT || 5007;
app.listen(PORT, () => {
    console.log(`Server berjalan di port ${PORT}`);
});
