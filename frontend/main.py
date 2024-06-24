import sys
import os
# sys.path.append('D:/Yoobee/Year 3/CS302 Assessment 3/aibee')
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import time
import re
import streamlit as st
from src.agents.report_generator import ReportGenerator
from src.agents.decision_taker import DecisionTaker
from src.agents.code_writer import CodeWriter

google_api_key = os.getenv('GOOGLE_API_KEY')

original_working_dir = os.getcwd()

# Loading messages icons
assistant_icon = "assets/assistant_icon.svg"
user_icon = "assets/user_icon_2.png"

st.set_page_config(layout="wide")

# Set custom CSS styling
with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Initalized messages, report content, and code content for managing state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, How can I help with your project?"}
    ]

if 'report_generated' not in st.session_state:
    st.session_state['report_generated'] = False
    st.session_state['buffer'] = None
    st.session_state['filename'] = None
    st.session_state['project_name'] = None

if 'report_area' not in st.session_state:
    st.session_state['report_area'] = " "

if 'code_area' not in st.session_state:
    st.session_state['code_area'] = []


def page_switcher(page):
    st.session_state.runpage = page

def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.01)


def workspace_page():
    api_key = google_api_key
    selected_model = "Gemini-Pro"

    #initializing agents
    decision_taker = DecisionTaker(selected_model, api_key)
    report_generator = ReportGenerator(selected_model, api_key)
    code_writer = CodeWriter(selected_model,api_key)

    #splitting the screen for report area and code area
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
                if st.session_state.filename:
                    st.session_state.filename
                    st.session_state.report_area
                    st.download_button(
                            label="Download Report Template",
                            data=st.session_state['buffer'],
                            file_name=st.session_state['filename'],
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

            with tab2:
                code_area = st.container()
                st.session_state.code_area
    
    #user prompt
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

                #Displaying messages for ordinary messages
                if response["function"] == "ordinary_conversation":
                    st.chat_message("ai", avatar=assistant_icon).write_stream(
                        stream_text(response["reply"])
                    )
                    st.session_state.messages.append(
                        {"role": "ai", "content": response["reply"]}
                    )

                # Generating plan,report and code template if coding project is recognised
                elif response["function"] == "coding_project":
                    st.chat_message("ai", avatar=assistant_icon).write_stream(stream_text("Generating report for your project"))
                    st.session_state.messages.append({"role":"ai","content":"Generating report for your project",})
                    time.sleep(0.002) 

                    
                    with st.spinner("Generating report..."):
                        generated_report = report_generator.execute(prompt)
                        model_reply, json_response = report_generator.parse_response(generated_report)
                        project_name = json_response["project"]
                        file_buffer, final_filename = report_generator.generate_report(generated_report, project_name)
            
                        st.session_state.report_generated = True
                        st.session_state.buffer = file_buffer
                        st.session_state.filename = final_filename
                    
                    # st.chat_message("ai", avatar=assistant_icon).write_stream(stream_text(model_reply))
                    # st.session_state.messages.append({"role":"ai","content":model_reply})

                    with report_area:
                        plan_and_summary = generated_report[generated_report.index("Plan"):-3]
                        st.session_state.report_area = plan_and_summary.replace("[ ]", "")
                        st.session_state.project_name = f"Project name: {project_name}" 
                        st.write_stream(stream_text(st.session_state.project_name))
                        st.write_stream(stream_text(st.session_state.report_area))
                        st.download_button(
                            label="Download Report Template",
                            data=st.session_state['buffer'],
                            file_name=st.session_state['filename'],
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

                    # report_generator.generate_report(generated_report,project_name)



                    with st.spinner("Generating the code ..."):
                        coder_output = code_writer.execute(
                            generated_report[
                                generated_report.index("Plan"): generated_report.index(
                                    "Summary"
                                )
                            ],
                            prompt,
                        )
                    
                    st.session_state.code_area = coder_output
                    with st.spinner("Generating code..."):
                        with code_area:
                            for item in st.session_state.code_area:
                                st.write_stream(
                                    stream_text(f"File name: {item['file']}")
                                )
                                st.write_stream(stream_text(item["code"]))

                    st.chat_message("ai", avatar=assistant_icon).write_stream(
                        stream_text(
                            f"I finished generating the code template for {project_name}. Check out the Code Template tab"
                        )
                    )
                    st.session_state.messages.append(
                        {
                            "role": "ai",
                            "content": f"I finished generating the code template for {project_name}. Check out the Code Template tab",
                        }
                    )
                    
                    
                    


if __name__ == "__main__":
    if "runpage" not in st.session_state:
        st.session_state.runpage = workspace_page
    st.session_state.runpage()



 