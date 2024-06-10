from flask import Flask, jsonify, request , render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'tugasduadwbi-tugasduadwbi.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_ZDlr9ve2e04PDMAixdK'
app.config['MYSQL_DB'] = 'collab'
app.config['MYSQL_PORT'] = 22273  

 
mysql = MySQL(app)

#buat nampilin list request
@app.route('/request')
def showrequest():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM request WHERE reqby = 'Pamungkas'")#jgn lupa diganti
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom,row)))
        cursor.close()
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405

@app.route('/request/<int:id>', methods=['GET'])
def get_request_by_id(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM request WHERE reqby = 'Pamungkas' AND idReq=%s" #jgn lupa diganti
        cursor.execute(query, (id,))
        
        karyawan = cursor.fetchone()
        
        if karyawan:
            kolom = [i[0] for i in cursor.description]
            karyawan_data = dict(zip(kolom, karyawan))
            cursor.close()
            return jsonify(karyawan_data), 200
        else:
            cursor.close()
            return jsonify({'error': 'Request tidak ditemukan'}), 404
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405

#buat bikin request baru

@app.route('/tambahrequest', methods=['POST'])
def tambah_karyawan():
    if request.method == 'POST':
        
        jenis = request.json['jenis']
        nama = request.json['nama']
        deskripsi = request.json['deskripsi']
        jumlah = request.json['jumlah']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO request (reqby, jenis, nama, deskripsi, jumlah, status ) VALUES ('Bahagia', %s, %s, %s, %s, 'Pending')" #Pamungkas nya jgn lupa diganti
        val = (jenis, nama, deskripsi, jumlah)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data Request berhasil ditambahkan'}), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405

#UPDATE 
@app.route('/updaterequest',methods=['PUT'])
def editkaryawan():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE request SET status = %s, appby = 'Bahagia' WHERE idReq = %s"  
        val = (data['status'],request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'data berhasil diubah'})
    

#DELETE
@app.route('/hapusrequest', methods=['DELETE'])
def deletekaryawan():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM request WHERE idReq = %s"
        val = (request.args['id'],)  
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'data berhasil dihapus'})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=5100)