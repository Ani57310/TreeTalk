from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.chatbot import answer_question

app = FastAPI(title="TreeTalk API")


# Allow the Next.js frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/")
def root():
    return {
        "message": "🌳 TreeTalk API is running!"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer, docs = answer_question(request.message)

    seen = set()
    sources = []

    for doc in docs:

        tree = doc.metadata["tree"]

        if tree not in seen:

            seen.add(tree)
            sources.append(tree)

    return ChatResponse(
        answer=answer,
        sources=sources,
    )


print("\n=== REGISTERED ROUTES ===")
for route in app.routes:
    print(route.path, route.methods)
print("=========================\n")