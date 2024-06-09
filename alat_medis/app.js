const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(bodyParser.json());

const uri = 'mongodb+srv://ganelajeisa:ganelajeisa@cluster0.4ula36n.mongodb.net/alat_medis';
let alatmedisCollection;

// Connect to MongoDB
MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(client => {
        const db = client.db('alat_medis');  // Ensure this is your actual database name
        alatmedisCollection = db.collection('alat_medis');
        console.log('Connected to Database');
    })
    .catch(error => console.error(error));

// Endpoint untuk mendapatkan data poliklinik
app.get('/alat_medis', (req, res) => {
    // Jalankan query untuk mengambil data dari collection Poliklinik
    alatmedisCollection.find({}, { projection: { _id: 0 } }).toArray()
        .then(results => {
            res.status(200).json(results); // Mengirimkan data alat_medis dalam bentuk JSON sebagai respons
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk menambah data klinik
app.post('/alat_medis', (req, res) => {
    const data = req.body;
    alatmedisCollection.insertOne(data)
        .then(result => {
            res.status(201).json(result.ops[0]); // Mengirimkan data alat_medis yang baru ditambahkan dalam bentuk JSON sebagai respons
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk menghapus data klinik berdasarkan ID
app.delete('/alat_medis/:id', (req, res) => {
    const id = req.params.id;
    alatmedisCollection.deleteOne({ _id: new ObjectId(id) })
        .then(result => {
            if (result.deletedCount > 0) {
                res.status(200).json({ message: 'alat medis deleted' }); // Mengirimkan pesan bahwa klinik telah dihapus sebagai respons
            } else {
                res.status(404).json({ error: 'alat medis not found' }); // Mengirimkan pesan bahwa klinik tidak ditemukan sebagai respons jika ID tidak ditemukan
            }
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk mengupdate data klinik berdasarkan ID
app.put('/alat_medis/:id', (req, res) => {
    const id = req.params.id;
    const data = req.body;
    alatmedisCollection.updateOne(
        { _id: new ObjectId(id) },
        { $set: data }
    )
        .then(result => {
            if (result.matchedCount > 0) {
                res.status(200).json({ message: 'alat medis updated' }); // Mengirimkan pesan bahwa klinik telah diupdate sebagai respons
            } else {
                res.status(404).json({ error: 'alat medis not found' }); // Mengirimkan pesan bahwa klinik tidak ditemukan sebagai respons jika ID tidak ditemukan
            }
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

const PORT = process.env.PORT || 5008;
app.listen(PORT, () => {
    console.log(`Server berjalan di port ${PORT}`);
});
