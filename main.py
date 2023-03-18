import datetime
import logging
import time
import os
from fastapi import BackgroundTasks, FastAPI, File, Header, Request, UploadFile, Response
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel
from mp4_to_mp3 import mp3
from files_del import delete_file
from redis_db.db import Redis_endpoints
logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s %(asctime)s %(message)s")



description = """
# YouTube to mp3
This online converter can:  
* **Convert youtube video to mp3 file**  
* **Convert mp4 file to mp3 file**    
# For developers
I'm begginer web developer, that's why I will be glad to hear your suggestions
## P.S
_Website is still under development_  
But you can use converter mp4 to mp3
"""
tags_metadata = [
    {
        "name": "upload",
        "description": "These requests were needed for mp4 to mp3 converter",
    }
]
app = FastAPI(
    title="YouTube to mp3 online converter",
    description=description,
    version="0.1.1",
    openapi_tags=tags_metadata
)
db = Redis_endpoints()
class Message(BaseModel):
    message: str
def write_in_log(ip_address: str, user_agent, request: dict):
    date_now = datetime.datetime.now()
    date_now_str: str = date_now.strftime('%m/%d/%y %H:%M:%S')
    url: str = request["url"]
    method: str = request["method"]
    body = request["body"]
    with open("log.log", "a") as log_file:
        log_file.write(f"Url: {url}, Method: {method}, IP: {ip_address}, User-Agent: {user_agent}, Date: {date_now_str}, Body: {body}\n")
    logging.info("Writing in logs was successful")

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
        content={"message": f"Unsuppoted format {exc.name}. I support only .mp4 format"}
    )

@app.post(
        "/backend.api/upload", 
        responses = {
            200: {"description": "`input .mp4 file`: `output .mp3 file`"},
            456:  {"model": Message, "description": "Unsuppoted format"}
        },
        summary="Upload user file. Convert mp4 to mp3 using moviepy. And returns mp3 file", 
        tags=["upload"],)
async def Mp4ToMp3(background_task: BackgroundTasks, request: Request, user_agent: str | None = Header(default=None), token: str = Header(default="test-token"), file: UploadFile = File(...)):
    """
    - `Mp4 file in input`

    - `Mp3 file in output`
    """
    delete_file()
    client_host = request.client.host
    name_file: str = file.filename
    background_task.add_task(write_in_log, ip_address=client_host, user_agent=user_agent, request={"url": "/backend.api/upload", "method": "POST", "body": name_file})
    file_typle = os.path.splitext(name_file)
    name_without_format: str = file_typle[0]
    if  file_typle[1] != ".mp4":
        raise Unikformaterror(name=file_typle[1])
    with open(f"unuseful_cache/{file.filename}", 'wb') as mp4_file:
        content = await file.read()
        mp4_file.write(content)
        mp4_file.close() 
    mp3(db, token, name=name_without_format)
    return FileResponse(f"unuseful_cache/{name_without_format}.mp3", filename=f"{name_without_format}.mp3", media_type="application/octet-stream")
