from app import app
from openAI import make_test_request


@app.route('/questions/generate', methods=['GET'])
def generate_question():
    question = make_test_request()
    return question