from flask import Flask, request, jsonify
import mysql.connector
import os
from flask_cors import CORS

db = mysql.connector.connect(
    host = 'localhost'
    username = 'root'
    password = ''
    database = 'myproject'
)

cursor = db.cursor(dictionary=True)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'images'

@app.route('/add-blogs', methods=['POST'])
def add_blog():
    title = request.form.get('title')
    content = request.form.get('content')
    image = request.files['image']

    if 'image' not in request.files:
        return 'image is not there in request'

    if image.filename == '':
        return 'no image is selected'
    
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filepath)

    sql = 'INSERT INTO blogs (title,content,image) VALUES (%s,%s,%s)'
    val =  (title,content,filepath)
    cursor.execute(sql,val)
    db.commit()

    return jsonify ({
        "status": "success",
        "message": "Blog added successfully!",
        "data": {
            "title": title,
            "content": content,
            "filepath": filepath
        }
    })

@app.route('/get-blogs', methods=['GET'])
def get_blog():
    page = int(request.args.get('page',1))
    limit = int(request.args.get('limt',8))
    offset = (page - 1) * limit

    sql = 'SELECT title,content,image FROM blogs ORDER BY id DESC LIMIT %s OFFSET %s'
    cursor.execute(sql,(limit,offset))
    blogs = cursor.fetchall()

    

    


