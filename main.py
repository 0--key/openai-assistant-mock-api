import time
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI()

# Define the request model
class CreateAssistantRequest(BaseModel):
    instructions: str
    name: str
    description: str
    tools: list
    model: str
    temperature: float
    top_p: float

# Define the response model (not strictly necessary, but for clarity)
class CreateAssistantResponse(BaseModel):
    id: str
    object: str
    created_at: int
    name: str
    description: str
    model: str
    instructions: str
    tools: list
    metadata: dict
    top_p: float
    temperature: float
    response_format: str

@app.post("/v1/assistants", response_model=CreateAssistantResponse)
def create_assistant(
    data: CreateAssistantRequest,
    authorization: str = Header(None),
    content_type: str = Header(None),
    openai_beta: str = Header(None)
):
    # Validate the Authorization header
    if authorization != "Bearer sk-the-mock-key-for-openai-simulation-on-localhost":
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Validate Content-Type header
    if content_type != "application/json":
        raise HTTPException(status_code=415, detail="Unsupported Media Type")

    # Validate OpenAI-Beta header
    if openai_beta != "assistants=v2":
        raise HTTPException(status_code=400, detail="Invalid OpenAI-Beta header")

    mock_response = CreateAssistantResponse(
        id="asst_abc123",
        object="assistant",
        created_at=int(time.time()),  # using current time for created_at
        name=data.name,
        description=data.description,
        model=data.model,
        instructions=data.instructions,
        tools=data.tools,
        metadata={},
        top_p=data.top_p,
        temperature=data.temperature,
        response_format="auto"
    )
    return mock_response
