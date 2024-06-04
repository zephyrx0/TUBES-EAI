from flask import Flask, jsonify, request, session, redirect, url_for, render_template
from flask_mysqldb import MySQL
from datetime import datetime
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = 'cobain'


# mysql config
app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_PORT'] = 26484
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'ulasan'
mysql = MySQL(app)




def create_response(data, status_code, message):
    response = {
        'timestamp': datetime.now().isoformat(),
        'status': status_code,
        'message': message,
        'data': data
    }
    return jsonify(response)


@app.route('/ulasan', methods=['GET', 'POST'])
def ulasan():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM ulasan")

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        cursor.close()
        return create_response(data, 200, 'Success')

    elif request.method == 'POST':
        try:
            # get data from request
            id_dokter = request.json['idDokter']
            id_user = request.json['idUser']
            nama_user = request.json['namaUser']
            nama_dokter = request.json['namaDokter']
            poli = request.json['poli']
            ulasan_text = request.json['ulasan']

            # Open connection and insert to db
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO ulasan (idDokter, idUser, namaUser, namaDokter, poli, ulasan) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (id_dokter, id_user, nama_user, nama_dokter, poli, ulasan_text)
            cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()

            return create_response(None, 201, 'Ulasan berhasil ditambahkan')
        except KeyError:
            return create_response(None, 400, 'Permintaan tidak valid: Kolom yang dibutuhkan tidak ada')


        
@app.route('/ulasan/<id_ulasan>', methods=['GET'])
def detailulasan(id_ulasan):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM ulasan WHERE idUlasan = %s"
    cursor.execute(sql, (id_ulasan,))
    column_names = [i[0] for i in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(column_names, row)))
    cursor.close()
    if data:
        return create_response(data, 200, 'Success')
    else:
        return create_response(None, 404, 'Not Found: Ulasan not found')





@app.route('/tambah_ulasan')
def tambah_ulasan():
    return render_template('tambah_ulasan.html')

@app.route('/detail_ulasan')
def detail_ulasan():
    return render_template('detail_ulasan.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3002)