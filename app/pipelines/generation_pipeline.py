from app.core.llm import llm

def generate_response(prompt: str):
    response = llm.complete(prompt)
    return response.text