from flask import Flask, request, jsonify, render_template, session
import openai
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')


thread_id = "thread_gZPlA6hYW4PgAPZiEMmraSck"
assistant_id = "asst_URvtuzD3LVeo9AW0wD7okXB9"


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
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": user_input}]
        # )
        # chat_response = response.choices[0].message.content

        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=user_input
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions="Please answer the questions using the knowledge provided in the file.",
        )

        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run.id)
            if run.status == "completed":
                break

        messages = list(client.beta.threads.messages.list(
            thread_id=thread_id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        chat_response = message_content.value
        session['chat_history'].append(
            {'role': 'assistant', 'content': chat_response})
    except Exception as e:
        chat_response = f"Error: {str(e)}"
        session['chat_history'].append(
            {'role': 'assistant', 'content': chat_response})

    session.modified = True
    return jsonify({'user_input': user_input, 'chat_response': chat_response})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
