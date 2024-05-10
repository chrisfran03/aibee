from openai import OpenAI
from dotenv import load_dotenv
import unittest
import time
import logging

load_dotenv()
client = OpenAI()


class TestOpenAIAssistantAPI(unittest.TestCase):
    thread_id = "thread_LrXOKLSwfQVXbC9zmt4PE4iZ"
    assis_id = "asst_URvtuzD3LVeo9AW0wD7okXB9"

    # def test_chat_completion_response_structure(self):
    #     messages = [{"role": "user", "content": "Say this is a test"}]
    #     response = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=messages,
    #         max_tokens=50
    #     )

    #     self.assertIsNotNone(response.id, "Response ID is None")
    #     self.assertEqual(response.object, "chat.completion")
    #     self.assertIsNotNone(response.created, "Response 'created' is None")
    #     self.assertGreater(len(response.choices), 0,
    #                        "No choices in the response")
    #     self.assertIsNotNone(response.usage, "Response 'usage' is None")

    def test_assistant_knowledge_retrieval(self):
        message = "Where is Christo from?"

        message = client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=message
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_id, assistant_id=self.assis_id
        )

        messages = list(client.beta.threads.messages.list(
            thread_id=self.thread_id, run_id=run.id))

        message_content = messages[0].content[0].text
        time.sleep(0.5)
        print(message_content.value)
        # self.assertGreater(len(message_content.value), 0,
        #                    "The assistant did not retrieve any knowledge.")
        self.assertIn("dora and della", message_content.value.lower(),
                      "Expected 'Dora and Della' not found in the response.")

# def test_assistant_knowledge_retrieval(self):

#     prompt = "What is the primary purpose of the document?"

#     response = openai.Assistant.retrieve(
#         assistant_id=assis_id,
#         thread_id=thread_id,
#         prompt=prompt,
#         max_tokens=100
#     )

#     # Verify the assistant retrieves relevant information
#     self.assertGreater(
#         len(response.choices[0].text), 0, "The assistant did not retrieve any knowledge.")
#     self.assertIn("primary purpose", response.choices[0].text.lower(
#     ), "Expected phrase not found in the response.")


if __name__ == '__main__':
    unittest.main()
