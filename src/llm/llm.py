import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


class LLM:
    def __init__(self, base_model, api_key) -> None:
        self.base_model = base_model

        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def inference(self, prompt):
        # global conversation_history
        # conversation_history.append({'role': 'user', 'parts': [prompt]})

        
        # Set safety settings for the request
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            # You can adjust other categories as needed
        }

        response = self.model.generate_content(prompt, safety_settings=safety_settings)

        try:
            # Check if the response contains text
            return response.text
        except ValueError:
            # If the response doesn't contain text, check if the prompt was blocked
            print("Prompt feedback:", response.prompt_feedback)
            # Also check the finish reason to see if the response was blocked
            print("Finish reason:", response.candidates[0].finish_reason)
            # If the finish reason was SAFETY, the safety ratings have more details
            print("Safety ratings:", response.candidates[0].safety_ratings)
            # Handle the error or return an appropriate message
            return "Error: Unable to generate content Gemini API"