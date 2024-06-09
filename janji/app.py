from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from flask.json.provider import DefaultJSONProvider

app = Flask(__name__)

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

@app.route('/janji', methods=['GET', 'POST'])
def janji():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        query = """
        SELECT j.janji_id, j.pasien_id, p.nama AS nama_pasien, j.dokter_id, d.nama AS nama_dokter, j.tanggal_janji, j.waktu_janji, j.keterangan
        FROM janji j
        JOIN pasien p ON j.pasien_id = p.pasien_id
        JOIN dokter d ON j.dokter_id = d.dokter_id
        """
        cursor.execute(query)
        kolom = [i[0] for i in cursor.description]
        data = [dict(zip(kolom, row)) for row in cursor.fetchall()]
        for item in data:
            tanggal_janji_date = item['tanggal_janji']
            if isinstance(tanggal_janji_date, datetime):
                item['tanggal_janji'] = tanggal_janji_date.strftime("%Y-%m-%d")
            waktu_janji_time = item['waktu_janji']
            if isinstance(waktu_janji_time, datetime):
                item['waktu_janji'] = waktu_janji_time.strftime("%H:%M:%S")
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.json
        pasien_id = data['pasien_id']
        dokter_id = data['dokter_id']
        tanggal_janji = data['tanggal_janji']
        waktu_janji = data['waktu_janji']
        keterangan = data['keterangan']
        
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO janji (pasien_id, dokter_id, tanggal_janji, waktu_janji, keterangan) VALUES (%s, %s, %s, %s, %s)"
        val = (pasien_id, dokter_id, tanggal_janji, waktu_janji, keterangan)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Janji berhasil dibuat'})

@app.route('/detailjanji/<int:janji_id>', methods=['GET'])
def detailjanji(janji_id):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM janji WHERE janji_id = %s"
        cursor.execute(sql, (janji_id,))
        result = cursor.fetchone()
        if result:
            janji = {
                'janji_id': result[0],
                'pasien_id': result[1],
                'dokter_id': result[2],
                'tanggal_janji': result[3].strftime("%Y-%m-%d") if isinstance(result[3], datetime) else str(result[3]),
                'waktu_janji': result[4].strftime("%H:%M:%S") if isinstance(result[4], datetime) else str(result[4]),
                'keterangan': result[5]
            }
            cursor.close()
            return jsonify(janji)
        else:
            cursor.close()
            return jsonify({'error': 'Janji not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/editjanji/<int:janji_id>', methods=['PUT'])
def editjanji(janji_id):
    data = request.get_json()
    if data:
        pasien_id = data.get('pasien_id')
        dokter_id = data.get('dokter_id')
        tanggal_janji = data.get('tanggal_janji')
        waktu_janji = data.get('waktu_janji')
        keterangan = data.get('keterangan')
        
        cursor = mysql.connection.cursor()
        sql = "UPDATE janji SET pasien_id = %s, dokter_id = %s, tanggal_janji = %s, waktu_janji = %s, keterangan = %s WHERE janji_id = %s"
        val = (pasien_id, dokter_id, tanggal_janji, waktu_janji, keterangan, janji_id)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'Data janji berhasil diperbarui'})
    else:
        return jsonify({'error': 'Data tidak ditemukan atau tidak lengkap'}), 400

@app.route('/deletejanji/<int:janji_id>', methods=['DELETE'])
def deletejanji(janji_id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM janji WHERE janji_id = %s"
    val = (janji_id,)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Data janji berhasil dihapus'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
