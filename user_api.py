from flask import Flask, request, jsonify
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from flask_cors import CORS
import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Myproject'
)

cursor = db.cursor(dictionary=True)

app = Flask(__name__)
app.secret_key = "super_secret_123"   # REQUIRED FOR SESSION
CORS(app, supports_credentials=True)


@app.route('/signup',methods=['POST'])
def signup():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"status": "error", "message": "Email already exists"}), 400 
    
    hashed_password = generate_password_hash(password)

    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (name, email, hashed_password)
    cursor.execute(sql, val)
    db.commit()

    return jsonify({"status": "success", "message": "User registered successfully"})


@app.route('/login',methods = ['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
    user = cursor.fetchone()

    if not user:
        print("emial fail")
        return jsonify({"status":"error","message":"Invalid Email"}),400
    
    if not check_password_hash(user['password'], password):
        print("password fail")
        return jsonify({"status": "error", "message": "Invalid password"}), 400
    
    print("Login Success")
    session['user'] = {
        "id": user['id'],
        "name": user['name'],
        "email": user['email']
    }

    return jsonify({
        "status": "success",
        "message": "Login successful",
        "user": session['user']      
    })
    

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"status": "success", "message": "Logged out"})

    
if __name__ == '__main__':
    app.run(debug=True, port=8000)