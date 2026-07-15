from fastapi import FastAPI

app = FastAPI(title="Size Compare Web Service")


@app.get("/health")
def health():
    return {"status": "ok"}
