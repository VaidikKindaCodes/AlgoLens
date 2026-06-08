from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AlgoLens Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok"}