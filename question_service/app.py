from flask import Flask, jsonify

app = Flask(__name__)


#example of service
@app.route('/questions/generate', methods=['GET'])
def generate_question():
    print("question service up")
    mock_response = {
        "question": "What is the largest planet in the Solar System?",
        "options": ["Earth", "Jupiter", "Mars", "Venus"],
        "answer": "Jupiter"
    }
    return jsonify(mock_response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
