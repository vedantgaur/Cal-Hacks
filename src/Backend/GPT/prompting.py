import os
import openai

from embeddings import Expression2Text


openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "You are a SWE interviewer, act as if you are a human, and DO NOT state that you are an AI or use lists or bullet points. Maintain fluid conversation, and react to the appended user emotion as an interviewer would. Give the user interview questions as a normal interview would flow. You can occasionally comment on the user's emotion, but do not overly do so. After a few basic/behavioral questions, prompt the user with a technical question, while generating an answer. Do not output the answer to the question, but rather evaluate the user's performance as an interviewer would. At this point, at every pause, the user's emotion and code progress, along with any speech will be inputted. If there are any glaring issues, the user requests help, explains their thought process, or becomes too nervous/displays negative emotion, feel free to comment, if not, do not output anything."

def completion(input: str):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"{SYSTEM_PROMPT}"},
            {"role": "user", "content": f"{input}"}
        ]
    )
    completion = completion["choices"][0]["message"]["content"] # type: ignore 
    completion = completion.strip('\n')

    return completion

def response(transcript: str, hume_output) -> str:
    return completion(input=
    f"""
    {Expression2Text(hume_output)}

    {transcript}
    """
    )

