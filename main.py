# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:40:52 2023

@author: grees
"""

import os
import urllib.parse as urlparse
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from redis import Redis
from openai import OpenAI

# Create Flask app
app = Flask(__name__)
CORS(app)

# Redis session config
redis_url = os.environ.get('REDIS_URL')
url = urlparse.urlparse(redis_url)
redis_instance = Redis(host=url.hostname, port=url.port, password=url.password)

app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis_instance
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")
Session(app)

# OpenAI client setup
client = OpenAI(
    api_key=os.environ['API_KEY'],
    organization=os.environ['OPENAI_ORG']
)

def ask_gpt(conversation_history):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        max_tokens=1024,
        temperature=0.5,
    )
    return response.choices[0].message.content

@app.route("/")
def ask_question():
    question = request.args.get("question")
    if not question:
        return jsonify({"error": "Missing 'question' parameter"}), 400

    # Initialize session history if not present
    if 'history' not in session:
        session['history'] = [
            {
                "role": "system",
                "content": "You are a Bible Expert and Pastor. Provide brief, compassionate, scripture-based guidance. Always include a relevant Bible verse and explanation. Do not include the question in the response. Do not offer legal, medical, or financial advice."
            }
        ]

    # Add user question to history
    session['history'].append({"role": "user", "content": question})

    # Get GPT response
    response_text = ask_gpt(session['history'])

    # Add bot response to history
    session['history'].append({"role": "assistant", "content": response_text})
    session.modified = True

    return jsonify({"response": response_text})

@app.route("/reset", methods=["POST"])
def reset_conversation():
    session.pop('history', None)
    return jsonify({"message": "Conversation history reset."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
