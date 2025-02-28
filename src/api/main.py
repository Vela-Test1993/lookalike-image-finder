from fastapi import FastAPI, HTTPException
from routes import homepage_router

app = FastAPI()

# Include the routers in the app
app.include_router(homepage_router, prefix="/api", tags=["Home Page"])