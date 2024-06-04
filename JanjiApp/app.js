//Menggunakan express
const express = require('express')
const mongoose = require('mongoose');
const cors = require('cors');

const session = require('express-session');
const cookieParser = require('cookie-parser');
const flash = require('connect-flash');

const app = express()
const port = 3001

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
const uri = 'mongodb+srv://ganelajeisa:ganelajeisa@cluster0.4ula36n.mongodb.net/janji';

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
app.get('/infojanji', async (req, res) => {
  try {
      // Mendapatkan koleksi 'janji'
      const janjiCollection = db.collection('janji');

      // Menjalankan kueri ke koleksi 'janji'
      const documents = await janjiCollection.find({}).toArray();
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

// Endpoint untuk mencari janji berdasarkan idJanji
app.get('/infojanji/:id', async (req, res) => {
  try {
      const id = req.params.id;

      // Mendapatkan koleksi 'janji'
      const janjiCollection = db.collection('janji');

      // Menjalankan kueri ke koleksi 'janji' berdasarkan ID
      const janji = await janjiCollection.findOne({ idJanji: id });

      if (!janji) {
          // Jika janji tidak ditemukan, kirim respons dengan status 404
          res.status(404).json({ error: 'Janji tidak ditemukan' });
          return;
      }

      // Mengirimkan respons JSON dengan data janji yang ditemukan
      res.json(janji);
  } catch (error) {
      console.error('Gagal mendapatkan data dari MongoDB Atlas:', error);
      // Mengirimkan respons kesalahan
      res.status(500).json({ error: 'Gagal mendapatkan data dari MongoDB Atlas' });
  }
});
 
app.listen(port, () => {
  console.log(`Layanan Manajemen Janji | listening at http://localhost:${port}`)
})