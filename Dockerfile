# Menggunakan image Python yang sudah ada di Docker Hub
FROM python:latest

# Mengatur direktori kerja di dalam container
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt .

# Menginstal dependencies Python
RUN pip install -r requirements.txt

# Menyalin seluruh kode sumber aplikasi ke dalam container
COPY . .

# Perintah yang akan dijalankan ketika container dijalankan
CMD ["py", "app.py"]
