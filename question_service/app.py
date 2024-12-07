from flask import Flask, jsonify
from config import Config
from open_ai.simple_request import make_test_request

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/questions/generate', methods=['GET'])
def generate_question():
    question = make_test_request()
    return question


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
