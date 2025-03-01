from fastapi import FastAPI, HTTPException
from routes import homepage_router

app = FastAPI()

app.include_router(homepage_router, prefix="/api", tags=["Home Page"])