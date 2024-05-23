from flask import Flask, request, jsonify, render_template, session
import openai
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')


@ app.route('/', methods=['GET'])
def index():
    return render_template('index.html', chat_history=session.get('chat_history', []))


@ app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json['user_input']
    if 'chat_history' not in session:
        session['chat_history'] = []

    session['chat_history'].append({'role': 'user', 'content': user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        chat_response = response.choices[0].message.content
        session['chat_history'].append(
            {'role': 'assistant', 'content': chat_response})
    except Exception as e:
        chat_response = f"Error: {str(e)}"
        session['chat_history'].append(
            {'role': 'assistant', 'content': chat_response})

    session.modified = True
    return jsonify({'user_input': user_input, 'chat_response': chat_response})


if __name__ == '__main__':
    app.run(debug=True)
