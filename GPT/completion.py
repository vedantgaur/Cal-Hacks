import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def completion(prompt: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    completion = completion["choices"][0]["message"]["content"] # type: ignore 
    completion = completion.strip('\n')

    return completion


print(completion("I need help deciding between tacos or pizza"))