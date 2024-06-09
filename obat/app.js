const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(bodyParser.json());

const uri = 'mongodb+srv://ganelajeisa:ganelajeisa@cluster0.4ula36n.mongodb.net/klinik';
let obatCollection;

// Connect to MongoDB
MongoClient.connect(uri)
    .then(client => {
        const db = client.db('klinik');  // Pastikan ini adalah nama database Anda yang sebenarnya
        obatCollection = db.collection('Obat');
        console.log('Connected to Database');
    })
    .catch(error => console.error(error));

// Endpoint untuk mendapatkan data obat
app.get('/obat', (req, res) => {
    // Jalankan query untuk mengambil data dari collection Obat
    obatCollection.find({}, { projection: { _id: 0 } }).toArray()
        .then(results => {
            res.status(200).json(results); // Mengirimkan data obat dalam bentuk JSON sebagai respons
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk menambah data obat
app.post('/obat', (req, res) => {
    const data = req.body;
    obatCollection.insertOne(data)
        .then(result => {
            res.status(201).json(result.ops[0]); // Mengirimkan data obat yang baru ditambahkan dalam bentuk JSON sebagai respons
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk menghapus data obat berdasarkan ID
app.delete('/obat/:id', (req, res) => {
    const id = req.params.id;
    obatCollection.deleteOne({ _id: new ObjectId(id) })
        .then(result => {
            if (result.deletedCount > 0) {
                res.status(200).json({ message: 'Obat deleted' }); // Mengirimkan pesan bahwa obat telah dihapus sebagai respons
            } else {
                res.status(404).json({ error: 'Obat not found' }); // Mengirimkan pesan bahwa obat tidak ditemukan sebagai respons jika ID tidak ditemukan
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
                res.status(200).json({ message: 'Obat updated' }); // Mengirimkan pesan bahwa obat telah diupdate sebagai respons
            } else {
                res.status(404).json({ error: 'Obat not found' }); // Mengirimkan pesan bahwa obat tidak ditemukan sebagai respons jika ID tidak ditemukan
            }
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

const PORT = process.env.PORT || 5007;
app.listen(PORT, () => {
    console.log(`Server berjalan di port ${PORT}`);
});
