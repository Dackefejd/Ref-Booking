from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List, Optional

from database import models, database
from . import schemas

app = FastAPI()


# --- CORS SETUP ---

# --- CORS SETUP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # I produktion ska detta begränsas
    allow_methods=["*"],
    allow_headers=["*"],
)