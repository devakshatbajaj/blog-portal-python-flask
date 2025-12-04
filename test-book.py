from flask import Flask, jsonify, request

app = Flask(__name__)


# Get all books
@app.route('/check', methods=['GET'])
def get_books():
    return jsonify({"Hello" : "test"})


if __name__ == '__main__':
    app.run(debug=True)