from typing import Annotated

from fastapi import FastAPI, Header
from httpx import AsyncClient
from pydantic import BaseModel


MD_PROMPT = """#Context
*You are a software engineer with expertise in writing prompts for GitHub Copilot.
*You MUST suggest a prompt optimized for a Github Copilot coding agent that accomplishes the objective provided in the user's messages.
*You MUST follow the guidelines provided below.

#Guidelines
*You MUST use strong directive words such as "MUST", "MUST NOT", "WILL", or "WILL NOT" in generated prompts.
*You MUST NOT use weak directive words such as "SHOULD", "SHOULD NOT", "CAN", "CAN NOT", "MAY", or "MAY NOT" in generated prompts.
*You MUST generate prompts in markdown format.
*You MUST include a summary section in generated prompts.
*You MUST provide specific instructions in generated prompts.
"""

GITHUB_URL = "https://api.githubcopilot.com/chat/completions"


class PromptRequest(BaseModel):
    messages: list["PromptMessages"]


class PromptMessages(BaseModel):
    role: str
    content: str


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, welcome to the PromptGen Github Copilot extension!"}


@app.post("/")
async def post(
    x_github_token: Annotated[str | None, Header()],
    prompt_request: PromptRequest,
):
    messages = prompt_request.messages

    messages.insert(
        0,
        {
            "role": "system",
            "content": MD_PROMPT
        }
    )

    headers = {
        'Authorization': f'Bearer {x_github_token}',
        'Content-Type': 'application/json'
    }
    body = {
        'messages': messages,
        'stream': True
    }
    async with AsyncClient() as client:
        async with client.stream("POST", GITHUB_URL, headers=headers, json=body) as response:
            pass
