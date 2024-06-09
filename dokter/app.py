from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from flask.json.provider import DefaultJSONProvider

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'rumahsakit'
app.config['MYSQL_PORT'] = 26484

mysql = MySQL(app)

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, timedelta):
            return str(obj)
        return super().default(obj)

app.json = CustomJSONProvider(app)

@app.route('/dokter', methods=['GET'])
def get_dokter():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM dokter")
    kolom = [i[0] for i in cursor.description]
    data = [dict(zip(kolom, row)) for row in cursor.fetchall()]
    cursor.close()
    return jsonify(data)

@app.route('/edit_dokter/<int:dokter_id>', methods=['GET', 'POST'])
def edit_dokter(dokter_id):
    cursor = mysql.connection.cursor()
    if request.method == 'GET':
        # Ambil data dokter dari database berdasarkan ID
        cursor.execute("SELECT * FROM dokter WHERE dokter_id = %s", (dokter_id,))
        dokter = cursor.fetchone()
        cursor.close()
        return render_template('edit_dokter.html', dokter=dokter)
    elif request.method == 'POST':
        # Ambil data yang diperbarui dari formulir
        nama = request.form['nama']
        poli = request.form['poli']
        # Update data dokter dalam database
        cursor.execute("UPDATE dokter SET nama = %s, poli = %s WHERE dokter_id = %s", (nama, poli, dokter_id))
        mysql.connection.commit()
        cursor.close()
        flash('Data dokter berhasil diperbarui!')
        return redirect(url_for('get_dokter'))


@app.route('/delete_dokter/<int:dokter_id>', methods=['DELETE'])
def delete_dokter(dokter_id):
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM dokter WHERE dokter_id = %s", (dokter_id,))
        mysql.connection.commit()
        cursor.close()
        flash('Data dokter berhasil dihapus!')
        return redirect(url_for('get_dokter'))
    else:
        return "Metode yang diperlukan tidak didukung untuk rute ini."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
