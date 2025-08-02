from fastapi import FastAPI
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.routes import auth, health, jobs, applications # Import new routers

app = FastAPI(
    title="Drona Job Portal API",
    description="API documentation for the Drona Job Portal."
)

# Include the routers
app.include_router(auth.router)
app.include_router(health.router)
app.include_router(jobs.router)
app.include_router(applications.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Drona Job Portal API"}
