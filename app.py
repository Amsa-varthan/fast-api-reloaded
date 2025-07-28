# app.py
from fastapi import FastAPI
import sys
import os

# --- Python Path Correction ---
# When running Uvicorn from the root directory, Python needs to know
# where to find your source code ('src') and database modules.
# This block adds the project's root directory to the system path.
# This ensures that imports like `from src.routes import auth` work correctly.
# It's a crucial step for a structured project layout.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# -----------------------------

# Now, Python can find the 'src' directory at the root.
from src.routes import auth
from src.routes import healthy

app = FastAPI(
    title="Drona Job Portal API",
    description="API documentation for the Drona Job Portal."
)

# Include the routers from your 'src/routes' directory
app.include_router(auth.router)
app.include_router(healthy.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Drona Job Portal API"}
