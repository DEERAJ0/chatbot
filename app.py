### Modified app.py
from flask import Flask, render_template, request, jsonify
from openrouter_api import get_recipe
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please ask a question."})

    try:
        response = get_recipe(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)