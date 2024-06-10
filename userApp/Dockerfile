# Gunakan image python versi terbaru sebagai base image
FROM python:latest

# Tentukan direktori kerja di dalam container
WORKDIR /usr/src/app

# Salin file requirements.txt ke dalam container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Salin semua file ke dalam container
COPY . .

# Expose port yang digunakan oleh aplikasi
EXPOSE 4999

# Perintah untuk menjalankan aplikasi
CMD [ "python", "app.py" ]
