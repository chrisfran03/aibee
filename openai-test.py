from openai import OpenAI
from dotenv import load_dotenv
import unittest

load_dotenv()
client = OpenAI()


class TestOpenAIAssistantAPI(unittest.TestCase):

    def test_assistant_response_structure(self):
        messages = [{"role": "user", "content": "Say this is a test"}]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=50
        )
        # sample_response = {
        #     "id": "chatcmpl-abc123",
        #     "object": "chat.completion",
        #     "created": 1677858242,
        #     "model": "gpt-3.5-turbo-0613",
        #     "usage": {
        #         "prompt_tokens": 13,
        #         "completion_tokens": 7,
        #         "total_tokens": 20
        #     },
        #     "choices": [
        #         {
        #             "message": {
        #                 "role": "assistant",
        #                 "content": "\n\nThis is a test!"
        #             },
        #             "logprobs": 1,
        #             "finish_reason": "stop",
        #             "index": 0
        #         }
        #     ]
        # }
        self.assertIsNotNone(response.id, "Response ID is None")
        self.assertEqual(response.object, "chat.completion")
        self.assertIsNotNone(response.created, "Response 'created' is None")
        self.assertGreater(len(response.choices), 0,
                           "No choices in the response")
        self.assertIsNotNone(response.usage, "Response 'usage' is None")


if __name__ == '__main__':
    unittest.main()
