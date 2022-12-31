import time
import sqlite3
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from mp4_to_mp3 import mp3
from files_del import delete_file

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
class Unikformaterror(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(Unikformaterror)
async def format_exception(request: Request, exc: Unikformaterror):
    return JSONResponse(
        status_code = 456,
        content={"message": f"Unsuppoted format {exc.name[-4:]}. I support only .mp4 format"}
    )
@app.get("/")
async def main_window():
    with open("frontend/index.html", "r") as file:
        answer = file.read()
    return HTMLResponse(answer)


@app.post("/backend.api/upload")
async def mp4ToMp3(file: UploadFile = File(...)):
    delete_file()
    name_file = file.filename
    name_without_format = name_file[:len(name_file)-4]
    if name_file[-4:] != ".mp4":
        raise Unikformaterror(name=name_file[-4:])
    with open(f"unuseful_cache/{file.filename}", 'wb') as mp4_file:
        content = await file.read()
        mp4_file.write(content)
        mp4_file.close() 
    
    mp3(name=name_without_format)

    return FileResponse(f"unuseful_cache/{name_without_format}.mp3", filename=f"{name_without_format}.mp3", media_type="application/octet-stream")
