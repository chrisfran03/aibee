from openai import OpenAI
import streamlit as st
import time
from dotenv import load_dotenv

# client = OpenAI()

# model = "gpt-3.5-turbo"


# def get_response(question):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": question}]
#     )
#     return response.choices[0].message.content


def main():
    st.title('Project Helper')
    user_input = st.text_input("Ask a question:")

    # if st.button('Send'):
    #     if user_input:
    #         response = get_response(user_input)
    #         st.text_area("Response:", value=response, height=300)
    #     else:
    #         st.error("Please enter a question.")


if __name__ == '__main__':
    main()
