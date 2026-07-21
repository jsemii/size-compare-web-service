from fastapi import FastAPI
from app.routers import auth, garment, wishlist

app = FastAPI(title="Size Compare Web Service")
app.include_router(auth.router)
app.include_router(garment.router)
app.include_router(wishlist.router)

@app.get("/health")
def health():
    return {"status": "ok"}
