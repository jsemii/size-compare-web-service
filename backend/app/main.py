from fastapi import FastAPI
from app.routers import auth, garment, wishlist, compare

app = FastAPI(title="Size Compare Web Service")
app.include_router(auth.router)
app.include_router(garment.router)
app.include_router(wishlist.router)
app.include_router(compare.router)

@app.get("/health")
def health():
    return {"status": "ok"}
