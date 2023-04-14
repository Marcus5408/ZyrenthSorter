import openai
from dotenv import load_dotenv
import os

# load the environment variables from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# create a variable to hold messages
message_history = [
        {"role": "system", "content": "You are Zyrenth, a helpful and friendly chatbot that is still in development. You will help the user sort the files on their  computer. You first ask them for their name, then ask for the location of the files they want to sort. You then ask them if they want to sort more files, and if they say yes, you ask them for the location of the files they want to sort. If they say no, you thank them for using ZyrenthSorter and wish them a good day."},
        {"role": "assistant", "content": "Hello! Im Zyrenth, here to help you sort your files. What is your name?"},
        {"role": "user", "content": "hello!"}
    ] 

# send the message to the OpenAI chat completion API
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message_history,
)

print(completion.choices[0].message)