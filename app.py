from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, uvicorn
from asyncio import sleep

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def waypoints_generator():
    yield "data: Before response\n\n"
    await sleep(10)
    yield "data: First response\n\n"
    await sleep(40)
    yield "data: Second response\n\n"
    await sleep(80)
    yield "data: Third response\n\n"
    yield "data: Last response\n\n"

@app.get("/get-waypoints")
async def root():
    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no"
    }
    return StreamingResponse(waypoints_generator(), media_type="text/event-stream", headers=headers)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
