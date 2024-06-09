const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(bodyParser.json());

const uri = 'mongodb+srv://ganelajeisa:ganelajeisa@cluster0.4ula36n.mongodb.net/klinik';
let klinikCollection;

MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(client => {
        const db = client.db('klinik');
        klinikCollection = db.collection('klinik');
        console.log('Connected to Database');
    })
    .catch(error => console.error(error));

// Endpoint untuk mendapatkan data klinik
app.get('/klinik', (req, res) => {
    klinikCollection.find({}, { projection: { _id: 0 } }).toArray()
        .then(results => {
            res.status(200).json(results);
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk mendapatkan data klinik berdasarkan klinik_id
app.get('/api/klinik/:klinik_id', async (req, res) => {
    const klinikId = req.params.klinik_id;
    try {
      const klinik = await klinikCollection.findOne({ klinik_id: klinikId }, { projection: { _id: 0 } });
      if (klinik) {
        res.status(200).json(klinik);
      } else {
        res.status(404).json({ error: 'Klinik tidak ditemukan' });
      }
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'Terjadi kesalahan pada server' });
    }
  });

  // Endpoint untuk mengupdate data klinik berdasarkan klinik_id
  app.put('/api/klinik/:klinik_id', async (req, res) => {
    const klinikId = req.params.klinik_id;
    const data = req.body;
    try {
      const result = await klinikCollection.updateOne(
        { klinik_id: klinikId },
        { $set: data }
      );
      if (result.modifiedCount > 0) {
        res.status(200).json({ message: 'Data klinik berhasil diperbarui' });
      } else {
        res.status(404).json({ error: 'Klinik tidak ditemukan' });
      }
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'Terjadi kesalahan pada server' });
    }
  });



// Endpoint untuk menambah data klinik
app.post('/klinik', (req, res) => {
    const data = req.body;
    klinikCollection.insertOne(data)
        .then(result => {
            res.status(201).json(result.ops[0]);
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

// Endpoint untuk mengupdate data klinik


// Endpoint untuk menghapus data klinik
app.delete('/delete_klinik/:id', (req, res) => {
    const id = req.params.id;
    klinikCollection.deleteOne({ _id: new ObjectId(id) })
        .then(result => {
            if (result.deletedCount > 0) {
                res.status(200).json({ message: 'Klinik deleted' });
            } else {
                res.status(404).json({ error: 'Klinik not found' });
            }
        })
        .catch(error => res.status(500).json({ error: error.message }));
});

const PORT = process.env.PORT || 5006;
app.listen(PORT, () => {
    console.log(`Server berjalan di port ${PORT}`);
});