from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    return "Server is running. Use upload.html to upload an image."

if __name__ == '__main__':
    app.run(debug=True)
