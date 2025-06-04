import cohere
from rich import print
from dotenv import dotenv_values
import os

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
env_vars = dotenv_values(env_path)

# Retrieve API Key
CohereAPIKey = env_vars.get("cohereAPIKey")

co = cohere.Client(api_key=CohereAPIKey)

# Known task/function keywords
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# System preamble
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.

You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook'.

*** Do not answer any query, just decide what kind of query is given to you. ***

-> Respond with 'general (query)' if a query can be answered by a LLM model (conversational AI chatbot) and doesn't require any up-to-date or real-time information.

-> Respond with 'realtime (query)' if a query cannot be answered by a LLM model (because they don't have realtime data) and requires up-to-date information.

-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', 'open whatsapp', etc.

-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but is specific to applications.

-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is unclear, mark it as general.

-> Respond with 'generate image (image prompt)' if a query is requesting to generate an image with given prompt like 'generate image of a lion wearing sunglasses in space'.

-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th June for mom's birthday'.

-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down, etc. but if the query is asking to do multiple system tasks, respond accordingly.

-> Respond with 'content (topic)' if a query is asking to write any type of content like applications, code, emails or anything else about a topic.

-> Respond with 'google search (topic)' if a query is asking to search a specific topic on Google but if the query is asking to search multiple topics, mention them all.

-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on YouTube but if the query is asking to search multiple topics, mention all.

*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp'.

*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis', respond with 'exit'.

*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above.
"""

# Example chat history for context
ChatHistory = [
    {"role": "User", "message": "How are you ?"},
    {"role": "Chatbot", "message": "general How are you ?"},
    {"role": "User", "message": "Do you like pizza ?"},
    {"role": "Chatbot", "message": "general Do you like pizza ?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "What is today's date and remind me that I have a dancing performance on 5th August 11 pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11 pm on 5th August for dancing performance."},
    {"role": "User", "message": "chat with me"},
    {"role": "Chatbot", "message": "general chat with me"},
]

def FirstLayerDMW(prompt: str = "test"):
    print("[DEBUG] Prompt:", prompt)

    try:
        response_obj = co.chat(
            model='command-r-plus',
            message=prompt,
            temperature=0.7,
            chat_history=ChatHistory,
            prompt_truncation='OFF',
            connectors=[],
            preamble=preamble,
        )

        response = response_obj.text.replace("\n", "")
        print("[DEBUG] Raw response:", response)

        response_list = [i.strip() for i in response.split(",")]
        print("[DEBUG] Split response:", response_list)

        # Filter based on known task/function keywords
        filtered_response = [
            task for task in response_list
            if any(task.lower().startswith(func) for func in funcs)
        ]
        print("[DEBUG] Filtered response:", filtered_response)

        # Handle unresolved queries
        if any("(query)" in item for item in filtered_response):
            print("[DEBUG] Unresolved (query) found, re-calling function.")
            return FirstLayerDMW(prompt=prompt)
        
        return filtered_response

    except Exception as e:
        print("[ERROR]", str(e))
        return []

if __name__ == "__main__":
    while True:
        try:
            user_input = input(">>> ")
            result = FirstLayerDMW(user_input)
            print(result)
        except KeyboardInterrupt:
            print("\n[INFO] Exiting...")
            break
