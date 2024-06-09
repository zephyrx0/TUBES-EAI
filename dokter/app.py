from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'rumahsakit'
app.config['MYSQL_PORT'] = 26484

mysql = MySQL(app)

@app.route('/dokter', methods=['GET'])
def get_dokter():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM dokter")
    kolom = [i[0] for i in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(kolom, row)))
    cursor.close()
    return jsonify(data)

@app.route('/tambah_dokter', methods=['POST'])
def tambah_dokter():
    nama = request.json['nama']
    poli = request.json['poli']

    cursor = mysql.connection.cursor()
    sql = "INSERT INTO dokter (nama, poli) VALUES (%s,%s)"
    val = (nama, poli)
    cursor.execute(sql, val)
    mysql.connection.commit()

    cursor.close()
    return jsonify({'message': 'data berhasil masuk'})

    

@app.route('/detaildokter/<int:dokter_id>', methods=['GET'])
def detaildokter(dokter_id):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM dokter WHERE dokter_id = %s"
        cursor.execute(sql, (dokter_id,))
        result = cursor.fetchone()
        if result:
            dokter = {
                'dokter_id': result[0],
                'nama': result[1],
                'poli': result[2]
            }
            cursor.close()
            return jsonify(dokter)
        else:
            cursor.close()
            return jsonify({'error': 'Dokter not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/editdokter/<int:dokter_id>', methods=['PUT'])
def editdokter(dokter_id):
    data = request.get_json()
    if data:
        nama = data.get('nama')
        poli = data.get('poli')
        
        cursor = mysql.connection.cursor()
        sql = "UPDATE dokter SET nama = %s, poli = %s WHERE dokter_id = %s"
        val = (nama, poli, dokter_id)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'Data dokter berhasil diperbarui'})
    else:
        return jsonify({'error': 'Data tidak ditemukan atau tidak lengkap'}), 400

@app.route('/deletedokter/<int:dokter_id>', methods=['DELETE'])
def deletedokter(dokter_id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM dokter WHERE dokter_id = %s"
    val = (dokter_id,)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Data dokter berhasil dihapus'})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5002, debug = True)
