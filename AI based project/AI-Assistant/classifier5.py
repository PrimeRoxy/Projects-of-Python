import json
import os
import openai 
from classifier8 import process_user_input

prompt_template = """
Prompt: You are entrusted with gracefully formatting data into JSON upon receiving input, which will then be utilized to invoke an API for executing a designated action. Your task involves crafting the JSON representation, initiating the API call, executing the specified action based on user input, and elegantly presenting the outcome.

"""

openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

action_detail_file = "action_details.json"


def process_user_output(user_query):
    user_data = process_user_input(action_detail_file,user_query)
    if not user_data:
        return None
    
    try:
        with open(action_detail_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Action details file not found.")
        return None
    
    output_response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": f"\"{user_data}\"and use this data for response\"{data}\" "}   
        ],
        temperature=0,
    )
    # print(output_response)
    response = output_response.choices[0].message.content.strip()
    print(response)


def main():
    while True:
        user_query = input("Please enter your query: ")
        process_user_output(user_query)
        if user_query.lower() == "exit":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()