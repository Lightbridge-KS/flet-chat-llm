import os
import openai
from openai import OpenAI


model_llm = "phi3.5"

client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="nokeyneeded"
)


class AssistantLocal01:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
        
    def get_response(self, user_text):
        self.user_text = user_text
        while True:
            # if user says stop, then breaking the loop
            if self.user_text == "stop":
                break
            
            # Storing the user question in the messages list
            self.messages.append({"role": "user", "content": self.user_text})

            # Setting the response from OpenAI API
            response= client.chat.completions.create(
                model=model_llm,
                messages= self.messages # Full Message
            )
 
            # returning the response
            response_str = response.choices[0].message.content
            
            # Appending the generated response so that AI remembers past responses
            self.messages.append({
                "role":"assistant", "content": response_str               
            })
            
            print(response_str)
            return response_str
    

if __name__ == "__main__":
    a1 = AssistantLocal01()
    a1.get_response("Hello")
    # a1.get_response("What is my name?")
    