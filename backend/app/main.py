import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, garment, wishlist, compare
from app.core.logging_middleware import LoggingMiddleware

logging.basicConfig(level=logging.INFO, format="%(message)s")

app = FastAPI(title="Size Compare Web Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(garment.router)
app.include_router(wishlist.router)
app.include_router(compare.router)
app.add_middleware(LoggingMiddleware)

@app.get("/health")
def health():
    return {"status": "ok"}