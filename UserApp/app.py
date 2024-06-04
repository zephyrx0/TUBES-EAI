from flask import Flask, jsonify, request, session, redirect, url_for, render_template
from flask_mysqldb import MySQL
from datetime import datetime
from flask import Flask, render_template
from flask import redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = 'cobain'


# mysql config
app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_PORT'] = 26484
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'user'
mysql = MySQL(app)




def create_response(data, status_code, message):
    response = {
        'timestamp': datetime.now().isoformat(),
        'status': status_code,
        'message': message,
        'data': data
    }
    return jsonify(response)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Ambil data dari form
        nama = request.form['namaUser']
        email = request.form['email']
        password = request.form['password']
        
        # Cek apakah email sudah ada dalam database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cur.fetchone()
        if user:
            return jsonify({"message": "Email already exists"}), 400
        
        # Tambahkan user baru ke database
        cur.execute("INSERT INTO user (namaUser, email, pass) VALUES (%s, %s, %s)",
                    (nama, email, password))
        mysql.connection.commit()
        cur.close()
        
        # Set session untuk user yang berhasil registrasi
        session['email'] = email

        # Return respons JSON untuk registrasi berhasil
        return jsonify({"message": "Registration successful"}), 200
    

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ambil data dari form
        email = request.form['email']
        password = request.form['password']
        
        # Cek apakah user ada dalam database dan passwordnya cocok
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s AND pass = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            # Set session untuk user yang berhasil login
            session['email'] = email
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    return jsonify({"message": "Login successful"}), 200

# # Dashboard route
# @app.route('/dashboard')
# def dashboard():
#     # Cek apakah user sudah login
#     if 'email' in session:
#         email = session['email']
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT namaUser FROM user WHERE email = %s", (email,))
#         nama = cur.fetchone()[0]
#         cur.close()
#         return render_template('dashboard.html', nama=nama)
#     else:
#         return redirect(url_for('login'))
    
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user")

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        cursor.close()
        return create_response(data, 200, 'Success')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3003)