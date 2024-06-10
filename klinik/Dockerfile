# Gunakan image node versi terbaru sebagai base image
FROM node:latest

# Tentukan direktori kerja di dalam container
WORKDIR /usr/src/app

# Salin file package.json dan package-lock.json ke dalam container
COPY package*.json ./

# Install dependencies
RUN npm install

# Salin semua file dari folder lokal ke dalam container
COPY . .

# Expose port yang digunakan oleh aplikasi
EXPOSE 5006

# Perintah untuk menjalankan aplikasi
CMD [ "node", "app.js" ]
