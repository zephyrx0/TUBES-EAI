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

    app.get('/obat', (req, res) => {
        obatCollection.find({}, { projection: { _id: 0 } }).toArray()
            .then(results => {
                res.status(200).json(results);
            })
            .catch(error => res.status(500).json({ error: error.message }));
    });
    

// app.post('/tambahobat', (req, res) => {
//     const { nama_obat, deskripsi, dosis, efek_samping } = req.body;
//     const newObat = { nama_obat, deskripsi, dosis, efek_samping };
//     obatCollection.insertOne(newObat, (err, result) => {
//         if (err) {
//             return res.status(500).json({ error: err.message });
//         }
//         res.json({ message: 'data berhasil masuk' });
//     });
// });

app.post('/tambahobat', (req, res) => {
    const data = req.body;
    obatCollection.insertOne(data)
        .then(result => {
            console.log('Insertion result:', result);
            res.status(201).json(result.ops[0]);
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

app.get('/detailobat/:obat_id', async (req, res) => {
    const obatId = req.params.obat_id;  // Use obat_id as string
    try {
        const obat = await obatCollection.findOne({ obat_id: obatId }, { projection: { _id: 0 } });
        if (obat) {
            res.status(200).json(obat);
        } else {
            res.status(404).json({ error: 'Obat tidak ditemukan' });
        }
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Terjadi kesalahan pada server' });
    }
});


  app.put('/editobat/:obat_id', (req, res) => {
    const { obat_id } = req.params;
    const { nama_obat, deskripsi, dosis, efek_samping } = req.body;
    
    const updateData = {
        nama_obat: nama_obat,
        deskripsi: deskripsi,
        dosis: dosis,
        efek_samping: efek_samping
    };

    obatCollection.updateOne(
        { obat_id: obat_id }, // filter dokumen berdasarkan obat_id
        { $set: updateData }, // data yang akan diperbarui
        (err, result) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.json({ message: 'Data obat berhasil diperbarui' });
        }
    );
});

  

app.delete('/deleteobat/:obat_id', (req, res) => {
    const { obat_id } = req.params;
    obatCollection.deleteOne({ obat_id: obat_id }, (err, result) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Data obat berhasil dihapus' });
    });
});

const PORT = process.env.PORT || 5007;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
