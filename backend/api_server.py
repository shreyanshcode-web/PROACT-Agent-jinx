from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import asyncio
import pandas as pd
import hashlib
import os
from typing import Optional

app = FastAPI()

# Path to CSV storing users
USER_DB_PATH = os.path.join(os.path.dirname(__file__), "users.csv")

# Load or create user DataFrame
if os.path.exists(USER_DB_PATH):
    users_df = pd.read_csv(USER_DB_PATH)
else:
    users_df = pd.DataFrame(columns=["username", "password_hash"])
    users_df.to_csv(USER_DB_PATH, index=False)

# Simple in‑memory queue for demo chat integration
message_queue: asyncio.Queue[str] = asyncio.Queue()

class Prompt(BaseModel):
    prompt: str

class AuthPayload(BaseModel):
    username: str
    password: str

def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def _save_users():
    users_df.to_csv(USER_DB_PATH, index=False)

@app.post("/api/signup")
async def signup(payload: AuthPayload):
    if payload.username in users_df["username"].values:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_row = {"username": payload.username, "password_hash": _hash_password(payload.password)}
    global users_df
    users_df = users_df.append(new_row, ignore_index=True)
    _save_users()
    return {"status": "created"}

@app.post("/api/login")
async def login(payload: AuthPayload):
    if payload.username not in users_df["username"].values:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    stored_hash = users_df.loc[users_df["username"] == payload.username, "password_hash"].iloc[0]
    if stored_hash != _hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # In a real app, return a JWT. Here we just echo the username as a token.
    return {"token": payload.username}

@app.post("/api/prompt")
async def receive_prompt(data: Prompt, token: Optional[str] = Depends(lambda: None)):
    """Receive a user prompt, put it in the queue, and echo it back.
    The token parameter is a placeholder for future auth checks.
    """
    await message_queue.put(data.prompt)
    return {"reply": f"You said: {data.prompt}"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
