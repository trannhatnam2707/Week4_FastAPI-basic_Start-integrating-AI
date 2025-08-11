from fastapi import FastAPI
from cors_config import configure_cors
from service import get_ai_response
from model import PromptRequest, PromptResponse


app = FastAPI()

# Cấu hình CORS
configure_cors(app)

# Route post 
@app.post("/ask", response_model=PromptResponse)
async def ask_ai(request: PromptRequest):
    reply= get_ai_response(request.prompt)
    return PromptResponse(prompt=request.prompt, reply=reply)
