from fastapi import FastAPI

app = FastAPI(title="CivicLens", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "CivicLens", "status": "ok", "version": "0.1.0"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
