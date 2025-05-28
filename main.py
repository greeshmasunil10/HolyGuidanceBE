import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Configure filesystem-based session
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")
Session(app)

# OpenAI client
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

    if 'history' not in session:
        session['history'] = [
            {
                "role": "system",
                "content": "You are a Bible Expert and compassionate Pastor. You are speaking with someone who is seeking personal or spiritual guidance and may come with follow-up questions or concerns over time.   Actively remember the context of the ongoing conversation. Use prior exchanges to better understand the person's situation and offer biblically grounded, empathetic guidance. Do not offer medical, legal, or financial advice. Always include a relevant verse from the Bible and briefly explain how it applies to the situation. Your responses should be concise, warm, and comforting—avoid sermons or overly long replies. Do NOT repeat or reference the user’s exact question in your reply. Focus on offering meaningful, scriptural insight and emotional support rooted in the Word of God. at the end add a bible verse that is relevant to the question asked. question asked is:",

            }
        ]

    session['history'].append({"role": "user", "content": question})
    response_text = ask_gpt(session['history'])
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
