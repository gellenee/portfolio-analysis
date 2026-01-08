from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import prices
import os

app = FastAPI(title = "Portfolio Analytics API")

#cors middleware to prevent single origin blocking
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_methods=["*"],
    allow_headers=["*"],
)

#connect routers to main app

app.include_router(prices.router, prefix = "/api")
#health check
@app.get("/api/health")
def health():
    return {"status": "ok"}

# only need to run main.py instead of uvicorn on terminal
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload = True
    )
