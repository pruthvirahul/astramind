from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from app.orchestrator import handle_query
from app.feedback import store_feedback

class FeedbackRequest(BaseModel):
    query: str
    response: str
    approved: bool

app = FastAPI(title="AstraMind Aerospace AI")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/ask")
def ask_ai(query: str):
    response = handle_query(query)
    return {"response": response}

@app.post("/feedback")
def feedback(req: FeedbackRequest):
    store_feedback(req.query, req.response, req.approved)
    return {"status": "Feedback stored"}