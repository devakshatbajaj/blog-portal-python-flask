from flask import Flask, request, jsonify
import os
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
CORS(app)

UPLOAD_FOLDER = 'images'

@app.route('/add-blog', methods=['POST'])
def upload_image():
    # print("reached here")

    title = request.form.get('title')
    content = request.form.get('content')
    image = request.files['image']

    # print("title:", title)
    # print("content:", content)

    if 'image' not in request.files:
        return "No image part in the request", 400

    
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

@app.route('/add-comment', methods=['POST'])
def add_comments():
    data = request.json
    blog_id = data['blog_id']
    name = data['name']
    comment = data['comment']

    sql = "INSERT INTO comments (blog_id,name,comment) VALUES (%s,%s,%s) "
    val = (blog_id,name,comment)
    cursor.execute(sql,val)
    db.commit()

    return jsonify({"message": "Comment added successfully"})


@app.route('/get-blog', methods=['GET'])
def get_blogs():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 8))
    offset = (page - 1) * limit

    # Get total number of blogs
    cursor.execute("SELECT COUNT(*) AS total FROM blog")
    total = cursor.fetchone()['total']

    # Fetch blogs for current page
    sql = "SELECT id, title, content, image FROM blog ORDER BY id DESC LIMIT %s OFFSET %s"
    cursor.execute(sql, (limit, offset))
    blogs = cursor.fetchall()


    return jsonify({
        "data": blogs,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit  # total pages
    })


@app.route('/get-blog/<int:id>', methods=['GET'])
def get_blog_detail(id):
    sql = "SELECT id, title, content, image FROM blog WHERE id = %s"
    cursor.execute(sql, (id,))
    blog = cursor.fetchone()
    if not blog:
        return jsonify({"error": "Blog not found"}), 404
    return jsonify(blog)

@app.route('/get-comments/<int:blog_id>', methods=['GET'])
def get_comments(blog_id):
    sql = "SELECT name, comment FROM comments WHERE blog_id = %s ORDER BY id DESC"
    cursor.execute(sql, (blog_id,))
    comments = cursor.fetchall()
    return jsonify(comments)


if __name__ == '__main__':
    app.run(debug=True)
