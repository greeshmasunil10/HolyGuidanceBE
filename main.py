# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:40:52 2023

@author: grees
"""


import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Create OpenAI client
client = OpenAI(
    api_key=os.environ['API_KEY'],
    organization=os.environ['OPENAI_ORG']
)

def ask_gpt(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a Bible Expert and Pastor. Provide brief, compassionate, scripture-based guidance. Always include a relevant Bible verse and explanation. Do not include the question in the response. Do not offer legal, medical, or financial advice.",
            },
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=1024,
        temperature=0.5,
    )
    return response.choices[0].message.content

@app.route("/")
def ask_question():
    question = request.args.get("question")
    if not question:
        return jsonify({"error": "Missing 'question' parameter"}), 400

    response = ask_gpt(question)
    return jsonify({"response": response})

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)