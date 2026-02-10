from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
from app.agent import app as agent_app  # import langgraph agent
import uvicorn

# 1. setup the API
app = FastAPI(title="Chameleon AI API")

# 2. allow the fronend to talk to us (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  #frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. defined the data format
class ChatRequest(BaseModel):
    query: str

# 4. the chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    print(f"Received query: {request.query}")
    
    # run the AI agent
    inputs = {"query": request.query}
    result = agent_app.invoke(inputs)
    
    return {
        "response": result['response'],
        "topic": result.get('detected_topic', 'Unknown')
    }

# 5. run the server
if __name__ == "__main__":
    print("--- Starting Chameleon AI Server ---")
    uvicorn.run(app, host="0.0.0.0", port=8000)