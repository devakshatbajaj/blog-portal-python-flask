from flask import Flask, request
import mysql.connector
import json
import os

db = mysql.connector.connect (
    host= 'localhost',
    user='root',
    password= '',
    database='myproject',
)

cursor = db.cursor()

tasks = []

UPLOAD_DIR = "images"

class SimplePostAPI(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        if self.path == "/add-blog":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            data = json.loads(post_data.decode())

            title = data.get("title")
            content = data.get("content")
            image_path = data.get("image")  

            print("Title:", title)
            print("Content:", content)
            print("Image path:", image_path)

            # Save the file
            file_path = os.path.join(UPLOAD_DIR, "1.png")

            with open(file_path, "wb") as f:
                f.write(image_path)

            print("file_path to upload", file_path)

            sql = "INSERT INTO blog (title, content, image) VALUES (%s, %s, %s)"
            val = (title, content, file_path)

            cursor.execute(sql, val)
            db.commit()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
    
            self.end_headers()
            response = {"status": "success", "message": "Task added successfully"}
            self.wfile.write(json.dumps(response).encode())


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), SimplePostAPI)
    print("POST API running at http://localhost:8000")
    server.serve_forever()

            