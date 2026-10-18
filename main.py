import time
import uuid

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-actksd.example.com"
EMAIL = "23f2004697@ds.study.iitm.ac.in"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_required_headers(request, call_next):
    start = time.perf_counter()
    request_id = str(uuid.uuid4())

    response = await call_next(request)

    elapsed = max(0.0, time.perf_counter() - start)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"

    return response

@app.get("/stats")
def stats(values: str = Query(...)):
    numbers = [int(value.strip()) for value in values.split(",")]

    if not numbers:
        return {
            "email": EMAIL,
            "count": 0,
            "sum": 0,
            "min": None,
            "max": None,
            "mean": 0.0,
        }

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
    }
