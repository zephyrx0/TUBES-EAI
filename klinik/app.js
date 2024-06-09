const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(bodyParser.json());

const uri = 'mongodb+srv://ganelajeisa:ganelajeisa@cluster0.4ula36n.mongodb.net/klinik';
let klinikCollection;

// Connect to MongoDB
MongoClient.connect(uri, { useUnifiedTopology: true })
    .then(client => {
        const db = client.db('klinik');
        klinikCollection = db.collection('klinik');
        console.log('Connected to Database');
    })
    .catch(error => console.error(error));

    app.get('/klinik', (req, res) => {
        klinikCollection.find({}, { projection: { _id: 0 } }).toArray()
            .then(results => {
                res.status(200).json(results);
            })
            .catch(error => res.status(500).json({ error: error.message }));
    });
    

// app.post('/tambahklinik', (req, res) => {
//     const { nama_klinik, deskripsi, dosis, efek_samping } = req.body;
//     const newklinik = { nama_klinik, deskripsi, dosis, efek_samping };
//     klinikCollection.insertOne(newklinik, (err, result) => {
//         if (err) {
//             return res.status(500).json({ error: err.message });
//         }
//         res.json({ message: 'data berhasil masuk' });
//     });
// });

app.post('/tambahklinik', (req, res) => {
    const data = req.body;
    klinikCollection.insertOne(data)
        .then(result => {
            console.log('Insertion result:', result);
            res.status(201).json(result.ops[0]);
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

app.get('/detailklinik/:klinik_id', async (req, res) => {
    const klinikId = req.params.klinik_id;  // Use klinik_id as string
    try {
        const klinik = await klinikCollection.findOne({ klinik_id: klinikId }, { projection: { _id: 0 } });
        if (klinik) {
            res.status(200).json(klinik);
        } else {
            res.status(404).json({ error: 'klinik tidak ditemukan' });
        }
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Terjadi kesalahan pada server' });
    }
});


  app.put('/editklinik/:klinik_id', (req, res) => {
    const { klinik_id } = req.params;
    const { nama_klinik, alamat_klinik, no_telepon} = req.body;
    
    const updateData = {
        nama_klinik: nama_klinik,
        deskripsi: alamat_klinik,
        dosis: no_telepon
    };

    klinikCollection.updateOne(
        { klinik_id: klinik_id }, // filter dokumen berdasarkan klinik_id
        { $set: updateData }, // data yang akan diperbarui
        (err, result) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.json({ message: 'Data klinik berhasil diperbarui' });
        }
    );
});

  

app.delete('/deleteklinik/:klinik_id', (req, res) => {
    const { klinik_id } = req.params;
    klinikCollection.deleteOne({ klinik_id: klinik_id }, (err, result) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Data klinik berhasil dihapus' });
    });
});

const PORT = process.env.PORT || 5006;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
