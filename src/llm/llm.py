import os
import google.generativeai as genai

class LLM:
    def __init__(self, base_model, api_key) -> None:
        self.base_model = base_model

        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def inference(self, prompt):
        # global conversation_history
        # conversation_history.append({'role': 'user', 'parts': [prompt]})

        response = self.model.generate_content(prompt).text

        # conversation_history.append({'role': 'model', 'parts': [response]})
        
        # print(conversation_history)

        return response