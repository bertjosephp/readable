import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import openai

# load environment variables from .env
load_dotenv()

# set up Flask app
app = Flask(__name__)
CORS(app)

# get OpenAI API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key! Make sure it's set in the .env file.")

# set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# route to simplify text
@app.route("/simplify", methods=["POST"])
def simplify_text():
    try:
        # get input text from the request
        data = request.get_json()
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # call OpenAI API to simplify the text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that simplifies text for a general audience."},
                {"role": "user", "content": f"Simplify this: {text}"}
            ],
            max_tokens=100,
            temperature=0.7,
        )

        # extract the simplified text from the response
        simplified_text = response['choices'][0]['message']['content'].strip()
        return jsonify({"simplified_text": simplified_text})

    except openai.OpenAIError as e:
        return jsonify({"error": f"an OpenAI error occurred: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"an unexpected error occurred: {str(e)}"}), 500

# run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
