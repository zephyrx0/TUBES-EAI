const express = require('express')
const mongoose = require('mongoose');
const cors = require('cors');

const session = require('express-session');
const cookieParser = require('cookie-parser');
const flash = require('connect-flash');

const app = express()
const port = 3000

//Menggunakan EJS
app.set('view engine', 'ejs');
app.use(express.urlencoded());
app.use(cors());

app.use(cookieParser('secret'));
app.use(session({
  cookie: { maxAge: 6000 },
  secret: 'secret',
  resave: true,
  saveUninitialized: true
}));
app.use(flash());

// URL koneksi MongoDB Atlas
const uri = 'mongodb+srv://ganelajeisa:ganelajeisa@cluster0.4ula36n.mongodb.net/dokter';

// Membuat koneksi ke MongoDB Atlas
mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true });

// Mendapatkan koneksi default
const db = mongoose.connection;

// Menangani peristiwa kesalahan
db.on('error', console.error.bind(console, 'Koneksi MongoDB gagal:'));

// Menangani peristiwa koneksi berhasil
db.once('open', async () => {
    console.log('Terhubung ke MongoDB Atlas');
});

// Definisikan endpoint HTTP dengan app.get()
app.get('/infodokter', async (req, res) => {
  try {
      // Mendapatkan koleksi 'dokter'
      const dokterCollection = db.collection('dokter');

      // Menjalankan kueri ke koleksi 'dokter'
      const documents = await dokterCollection.find({}).toArray();
      console.log('Data dari koleksi:');
      console.log(documents);

      // Mengirimkan respons JSON dengan data yang ditemukan
      res.json(documents);
  } catch (error) {
      console.error('Gagal mendapatkan data dari MongoDB Atlas:', error);
      // Mengirimkan respons kesalahan
      res.status(500).json({ error: 'Gagal mendapatkan data dari MongoDB Atlas' });
  }
});

// Endpoint untuk mencari dokter berdasarkan idDokter
app.get('/infodokter/:id', async (req, res) => {
  try {
      const id = req.params.id;

      // Mendapatkan koleksi 'dokter'
      const dokterCollection = db.collection('dokter');

      // Menjalankan kueri ke koleksi 'dokter' berdasarkan ID
      const dokter = await dokterCollection.findOne({ idDokter: id });

      if (!dokter) {
          // Jika dokter tidak ditemukan, kirim respons dengan status 404
          res.status(404).json({ error: 'Dokter tidak ditemukan' });
          return;
      }

      // Mengirimkan respons JSON dengan data dokter yang ditemukan
      res.json(dokter);
  } catch (error) {
      console.error('Gagal mendapatkan data dari MongoDB Atlas:', error);
      // Mengirimkan respons kesalahan
      res.status(500).json({ error: 'Gagal mendapatkan data dari MongoDB Atlas' });
  }
});
 
app.listen(port, () => {
  console.log(`Layanan Manajemen Janji | listening at http://localhost:${port}`)
})