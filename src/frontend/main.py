from fastapi import FastAPI
from starlette import status
from starlette.responses import Response, FileResponse

import uvicorn

import threading
import os

app = FastAPI()

@app.get("/")
async def index():
    file = os.path.join(os.getcwd(), "src/frontend/index.html")
    return FileResponse(file)

@app.get("/ping")
async def ping():
    return Response(status_code=status.HTTP_200_OK)

@app.get("/{_filename}")
async def getfile(_filename: str):
    file = os.path.join(os.getcwd(), "src/frontend", _filename)
    return FileResponse(file)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)