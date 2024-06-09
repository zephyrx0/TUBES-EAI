const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(bodyParser.json());

const uri = 'mongodb+srv://ganelajeisa:ganelajeisa@cluster0.4ula36n.mongodb.net/alat';
let alatCollection;

// Connect to MongoDB
MongoClient.connect(uri, { useUnifiedTopology: true })
    .then(client => {
        const db = client.db('alat');
        alatCollection = db.collection('alat');
        console.log('Connected to Database');
    })
    .catch(error => console.error(error));

    app.get('/alat', (req, res) => {
        alatCollection.find({}, { projection: { _id: 0 } }).toArray()
            .then(results => {
                res.status(200).json(results);
            })
            .catch(error => res.status(500).json({ error: error.message }));
    });

app.post('/tambahalat', (req, res) => {
    const data = req.body;
    alatCollection.insertOne(data)
        .then(result => {
            console.log('Insertion result:', result);
            res.status(201).json(result.ops[0]);
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

app.get('/detailalat/:alat_id', async (req, res) => {
    const alat_id = req.params.alat_id;  // Use alat_id as string
    try {
        const alat = await alatCollection.findOne({ alat_id: alat_id }, { projection: { _id: 0 } });
        if (alat) {
            res.status(200).json(alat);
        } else {
            res.status(404).json({ error: 'alat tidak ditemukan' });
        }
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Terjadi kesalahan pada server' });
    }
});


  app.put('/editalat/:alat_id', (req, res) => {
    const { alat_id } = req.params;
    const { nama_alat, deskripsi, jumlah} = req.body;
    
    const updateData = {
        nama_alat: nama_alat,
        deskripsi: deskripsi,
        jumlah: jumlah
    };

    alatCollection.updateOne(
        { alat_id: alat_id }, // filter dokumen berdasarkan alatmedisk_id
        { $set: updateData }, // data yang akan diperbarui
        (err, result) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.json({ message: 'Data alat medis berhasil diperbarui' });
        }
    );
});

  

app.delete('/deletealat/:alat_id', (req, res) => {
    const { alat_id } = req.params;
    alatCollection.deleteOne({ alat_id: alat_id }, (err, result) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Data alat medis berhasil dihapus' });
    });
});

const PORT = process.env.PORT || 5008;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
