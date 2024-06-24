from openai import OpenAI
from dotenv import load_dotenv
import time
import logging
from datetime import datetime
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI


load_dotenv()

client = OpenAI()

# == Creating assistant with the file search tool option enabled == #
# assistant = client.beta.assistants.create(
#     name="Knowledge Retrieval Assistant",
#     instructions="You are an assistant which retrieves data from the given text file and provides output exactly as instructed word by word.",
#     model="gpt-3.5-turbo",
#     tools=[{"type": "file_search"}],
# )
# print(assistant.id)


# == Hardcoded ids to be used once the first code run is done and the assistant was created
thread_id = ""
assis_id = ""

# # == Creating vector store for the uploaded file == #
# vector_store = client.beta.vector_stores.create(name="Random message")

# # Ready the files for upload to OpenAI
# file_paths = ["./random_message.txt"]
# file_streams = [open(path, "rb") for path in file_paths]

# # Use the upload and poll SDK helper to upload the files, add them to the vector store,
# # and poll the status of the file batch for completion.
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#     vector_store_id=vector_store.id, files=file_streams
# )

# # Print the status and the file counts of the batch to see the result of this operation.
# print(file_batch.status)
# print(file_batch.file_counts)


# Upload the user provided file to OpenAI
# message_file = client.files.create(
#     file=open("./random_message.txt", "rb"), purpose="assistants"
# )
# == Step 3. Create a Thread == #

# Create a thread and attach the file to the message
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "What are the names of Christo's of pets?",
#             # Attach the new file to the message.
#             "attachments": [
#                 {"file_id": message_file.id, "tools": [
#                     {"type": "file_search"}]}
#             ],
#         }
#     ]
# )

# # The thread now has a vector store with that file in its tool resources.
# print(thread.tool_resources.file_search)
# print(thread.id)
# message = "What is the secret word's first letter?"

# message = client.beta.threads.messages.create(
#     thread_id=thread_id, role="user", content=message
# )

# run = client.beta.threads.runs.create_and_poll(
#     thread_id=thread_id, assistant_id=assis_id
# )

# messages = list(client.beta.threads.messages.list(
#     thread_id=thread_id, run_id=run.id))

# message_content = messages[0].content[0].text

# print(message_content.value)
# print(type(message_content.value))

# run = client.beta.threads.runs.create(
#     thread_id=thread_id,
#     assistant_id=assis_id,
#     # instructions="The document random_message.txt contains the information you need .Only provide the output with the information that you have from this file",
# )
