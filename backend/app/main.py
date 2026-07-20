from fastapi import FastAPI
from app.routers import auth, garment

app = FastAPI(title="Size Compare Web Service")
app.include_router(auth.router)
app.include_router(garment.router)

@app.get("/health")
def health():
    return {"status": "ok"}
