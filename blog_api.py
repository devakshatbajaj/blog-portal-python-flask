from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='myproject'
)

cursor = db.cursor(dictionary=True)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'images'

@app.route('/add-blog', methods=['POST'])
def upload_image():
    print("reached here")

    title = request.form.get('title')
    content = request.form.get('content')

    print("title:", title)
    print("content:", content)

    if 'image' not in request.files:
        return "No image part in the request", 400

    image = request.files['image']
    if image.filename == '':
        return "No image selected", 400

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Save file to folder
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filepath)

    # Save to database (store file path, not file object)
    sql = "INSERT INTO blog (title, content, image) VALUES (%s, %s, %s)"
    values = (title, content, filepath)
    cursor.execute(sql, values)
    db.commit()

    return jsonify({
        "status": "success",
        "message": "Blog added successfully!",
        "data": {
            "title": title,
            "content": content,
            "filepath": filepath
        }
    })

@app.route('/get-blog', methods=['GET'])
def get_blogs():

    sql = "SELECT id, title, content, image FROM blog ORDER BY id DESC"
    cursor.execute(sql)
    blogs = cursor.fetchall()

    return jsonify(blogs)

@app.route('/get-blog/<int:id>', methods=['GET'])
def get_blog_detail(id):
    sql = "SELECT id, title, content, image FROM blog WHERE id = %s"
    cursor.execute(sql, (id,))
    blog = cursor.fetchone()
    if not blog:
        return jsonify({"error": "Blog not found"}), 404
    return jsonify(blog)



if __name__ == '__main__':
    app.run(debug=True)
