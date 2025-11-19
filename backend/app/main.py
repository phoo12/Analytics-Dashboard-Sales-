from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.database.database import engine, Base


# load env varibles

load_dotenv() 

# create database tables

Base.metadata.create_all(bind=engine)

#  create fastapi app

app = FastAPI(
     title="Analytics Dashboard API",
    description="Backend API for Analytics Dashboard",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Next.js frontend
    "http://127.0.0.1:3000",
    "http://localhost:3003",  # Next.js frontend
    "http://127.0.0.1:3003",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# include API routes
app.include_router(router, prefix="/api", tags=["analytics"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])  # ← ADD THIS LINE

#  root endpoint

@app.get("/")
async def root():
    return{
        "message": "Analytics Dashboard API",
        "status": "running",
        "version": "1.0.0"
    }

# health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
