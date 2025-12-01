from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import asyncio
import os
from typing import Optional

# DB
from jinx.db.session import init_db, get_session
from jinx.db.models import User

# Password hashing
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

init_db()

app = FastAPI()

# Simple in‑memory queue for demo chat integration
message_queue: asyncio.Queue[str] = asyncio.Queue()


class Prompt(BaseModel):
    prompt: str


class AuthPayload(BaseModel):
    username: str
    password: str


def hash_password(pw: str) -> str:
    return pwd_context.hash(pw)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        return False



@app.post("/api/signup")
async def signup(payload: AuthPayload):
    session = get_session()
    try:
        # check existing
        existing = session.query(User).filter(User.username == payload.username).first()
        if existing is not None:
            raise HTTPException(status_code=400, detail="Username already exists")
        user = User(username=payload.username, password_hash=hash_password(payload.password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": "created", "user": user.as_dict()}
    finally:
        session.close()

@app.post("/api/login")
async def login(payload: AuthPayload):
    session = get_session()
    try:
        user = session.query(User).filter(User.username == payload.username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        # In a real app, return a JWT. Here we just echo the username as a token.
        return {"token": payload.username}
    finally:
        session.close()

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
