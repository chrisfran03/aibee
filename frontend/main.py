import sys
sys.path.append('D:/Yoobee/Year 3/CS302 Assessment 3/aibee')
import os
import time
import streamlit as st
# from utils import stream_text, search_queries, prepare_coding_files
# from src.keyword_extractor import SentenceBert
# from src.agents.project_creator import ProjectCreator
# from src.agents.coder import Coder
# from src.agents.researcher import Researcher
# from src.agents.planner import Planner
from src.agents.decision_taker import DecisionTaker

google_api_key = os.getenv('GOOGLE_API_KEY')

original_working_dir = os.getcwd()

# Loading messages icons
assistant_icon = "assets/assistant_icon.svg"
user_icon = "assets/user_icon_2.png"

st.set_page_config(layout="wide")

# Set custom CSS styling
with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Initalized messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, How can I help with your project?"}
    ]

def page_switcher(page):
    st.session_state.runpage = page

def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.01)


def workspace_page():
    api_key = google_api_key
    selected_model = "Gemini-Pro"

    decision_taker = DecisionTaker(selected_model, api_key)
    # planner = Planner(selected_model, api_key)
    # reseacher = Researcher(selected_model, api_key)
    # coder = Coder(selected_model, api_key)
    # project_creator = ProjectCreator(selected_model, api_key)

    col1, col2 = st.columns(2)

    with col2:
        workspace = st.container(height=600,border=True)
        with workspace:
            st.title("Workspace", anchor=False)
            tab1, tab2 = st.tabs(
                ["Report Template", "Code Template"]
            )

            with tab1:
                report_area = st.container()

            with tab2:
                code_area = st.container()
    
    prompt = st.chat_input(placeholder="Talk to assistant")

    with col1:
        chat = st.container(height=600, border =True)

        with chat:
            st.title("Chat with assistant", anchor= False)

            # Displaying messages
            for message in st.session_state.messages:
                icon = user_icon if message["role"] == "user" else assistant_icon
                st.chat_message(message["role"], avatar=icon).write(
                    message["content"]
                )

            #Processing user prompt
            if prompt:
                st.chat_message("user", avatar=user_icon).write(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.spinner("Processing your prompt ..."):
                    response = decision_taker.execute(prompt)[0]

                if response["function"] == "ordinary_conversation":
                    st.chat_message("ai", avatar=assistant_icon).write_stream(
                        stream_text(response["reply"])
                    )
                    st.session_state.messages.append(
                        {"role": "ai", "content": response["reply"]}
                    )    



if __name__ == "__main__":
    if "runpage" not in st.session_state:
        st.session_state.runpage = workspace_page
    st.session_state.runpage()



#      # Importing required packages
# import streamlit as st
# import time
# from openai import OpenAI

# # Set your OpenAI API key and assistant ID here
# api_key         = st.secrets["openai_apikey"]
# assistant_id    = st.secrets["assistant_id"]

# # Set openAi client , assistant ai and assistant ai thread
# @st.cache_resource
# def load_openai_client_and_assistant():
#     client          = OpenAI(api_key=api_key)
#     my_assistant    = client.beta.assistants.retrieve(assistant_id)
#     thread          = client.beta.threads.create()

#     return client , my_assistant, thread

# client,  my_assistant, assistant_thread = load_openai_client_and_assistant()

# # check in loop  if assistant ai parse our request
# def wait_on_run(run, thread):
#     while run.status == "queued" or run.status == "in_progress":
#         run = client.beta.threads.runs.retrieve(
#             thread_id=thread.id,
#             run_id=run.id,
#         )
#         time.sleep(0.5)
#     return run

# # initiate assistant ai response
# def get_assistant_response(user_input=""):

#     message = client.beta.threads.messages.create(
#         thread_id=assistant_thread.id,
#         role="user",
#         content=user_input,
#     )

#     run = client.beta.threads.runs.create(
#         thread_id=assistant_thread.id,
#         assistant_id=assistant_id,
#     )

#     run = wait_on_run(run, assistant_thread)

#     # Retrieve all the messages added after our last user message
#     messages = client.beta.threads.messages.list(
#         thread_id=assistant_thread.id, order="asc", after=message.id
#     )

#     return messages.data[0].content[0].text.value


# if 'user_input' not in st.session_state:
#     st.session_state.user_input = ''

# def submit():
#     st.session_state.user_input = st.session_state.query
#     st.session_state.query = ''


# st.title("🍕 Papa Johns Pizza Assistant 🍕")

# st.text_input("Play with me:", key='query', on_change=submit)

# user_input = st.session_state.user_input

# st.write("You entered: ", user_input)

# if user_input:
#     result = get_assistant_response(user_input)
#     st.header('Assistant :blue[cool] :pizza:', divider='rainbow')
#     st.text(result)