const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(bodyParser.json());

const uri = 'mongodb+srv://ganelajeisa:ganelajeisa@cluster0.4ula36n.mongodb.net/klinik';
let klinikCollection;

// Connect to MongoDB
MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(client => {
        const db = client.db('klinik');  // Ensure this is your actual database name
        klinikCollection = db.collection('klinik');
        console.log('Connected to Database');
    })
    .catch(error => console.error(error));

// Endpoint untuk mendapatkan data poliklinik
app.get('/klinik', (req, res) => {
    // Jalankan query untuk mengambil data dari collection Poliklinik
    klinikCollection.find({}, { projection: { _id: 0 } }).toArray()
        .then(results => {
            res.status(200).json(results); // Mengirimkan data poliklinik dalam bentuk JSON sebagai respons
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk menambah data klinik
app.post('/klinik', (req, res) => {
    const data = req.body;
    klinikCollection.insertOne(data)
        .then(result => {
            res.status(201).json(result.ops[0]); // Mengirimkan data klinik yang baru ditambahkan dalam bentuk JSON sebagai respons
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk menghapus data klinik berdasarkan ID
app.delete('/klinik/:id', (req, res) => {
    const id = req.params.id;
    klinikCollection.deleteOne({ _id: new ObjectId(id) })
        .then(result => {
            if (result.deletedCount > 0) {
                res.status(200).json({ message: 'Klinik deleted' }); // Mengirimkan pesan bahwa klinik telah dihapus sebagai respons
            } else {
                res.status(404).json({ error: 'Klinik not found' }); // Mengirimkan pesan bahwa klinik tidak ditemukan sebagai respons jika ID tidak ditemukan
            }
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk mengupdate data klinik berdasarkan ID
app.put('/klinik/:id', (req, res) => {
    const id = req.params.id;
    const data = req.body;
    klinikCollection.updateOne(
        { _id: new ObjectId(id) },
        { $set: data }
    )
        .then(result => {
            if (result.matchedCount > 0) {
                res.status(200).json({ message: 'Klinik updated' }); // Mengirimkan pesan bahwa klinik telah diupdate sebagai respons
            } else {
                res.status(404).json({ error: 'Klinik not found' }); // Mengirimkan pesan bahwa klinik tidak ditemukan sebagai respons jika ID tidak ditemukan
            }
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

const PORT = process.env.PORT || 5006;
app.listen(PORT, () => {
    console.log(`Server berjalan di port ${PORT}`);
});
