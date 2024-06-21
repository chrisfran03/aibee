import sys
sys.path.append('D:/Yoobee/Year 3/CS302 Assessment 3/aibee')
import os
import time
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

            with tab2:
                code_area = st.container()
    
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

                    # st.chat_message("ai", avatar=assistant_icon).write_stream(stream_text(model_reply))
                    # st.session_state.messages.append({"role":"ai","content":model_reply})

                    with report_area:
                        plan_and_summary = generated_report[generated_report.index("Plan"):-3]
                        st.write_stream(stream_text(f"Project name: {project_name}"))
                        st.write_stream(stream_text(plan_and_summary.replace("[ ]", "")))

                    report_generator.generate_report(generated_report,project_name)

                    with st.spinner("Generating the code ..."):
                        coder_output = code_writer.execute(
                            generated_report[
                                generated_report.index("Plan"): generated_report.index(
                                    "Summary"
                                )
                            ],
                            prompt,
                        )

                    with st.spinner("Generating code..."):
                        with code_area:
                            for item in coder_output:
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



 