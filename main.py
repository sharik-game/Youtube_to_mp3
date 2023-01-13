import datetime
import logging
import time
from fastapi import BackgroundTasks, FastAPI, File, Header, Request, UploadFile, Response
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from mp4_to_mp3 import mp3
from files_del import delete_file
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
    },
    {
        "name": "main",
        "description": "These requests were needed for **main site page**"
    }
]
app = FastAPI(
    title="YoTube to mp3 online converter",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)

def write_in_log(ip_address: str, user_agent, request: dict):
    date_now = datetime.datetime.now()
    date_now_str: str = date_now.strftime('%m/%d/%y %H:%M:%S')
    url: str = request["url"]
    method: str = request["method"]
    body = request["body"]
    with open("log.txt", "a") as log_file:
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
        content={"message": f"Unsuppoted format {exc.name[-4:]}. I support only .mp4 format"}
    )

@app.get("/", summary="Main site page", tags=["main"])
async def main_page(request: Request, background_task: BackgroundTasks, user_agent: str | None = Header(default=None)):
    client_host = request.client.host
    background_task.add_task(write_in_log, ip_address=client_host, user_agent=user_agent, request={"url": "/", "method": "GET", "body": None})
    with open("frontend/main_site_page/index.html", "r") as main_file:
        answer = main_file.read()
    return HTMLResponse(answer)
@app.get("/frontend/main_site_page/main_page.js", tags=["main"])
async def read_main_js():
    with open("frontend/main_site_page/main_page.js", "r") as main_pagejs:
        ans = main_pagejs.read()
    return Response(content=ans, media_type="text/javascript")

@app.get("/upload", summary="Return HTML page for mp4 to mp3 converter", tags=["upload"])
async def main_window(request: Request, background_tasks: BackgroundTasks, user_agent: str | None = Header(default=None)):
    client_host = request.client.host
    background_tasks.add_task(write_in_log, ip_address=client_host, user_agent=user_agent, request={"url": "/upload/", "method": "GET", "body": None})
    with open("frontend/upload2/upload.html", "r") as file:
        answer = file.read()
    return HTMLResponse(answer)
@app.get("/frontend/upload2/upload1.js", tags=["upload"])
async def read_upload_js():
    with open("frontend/upload2/upload1.js", "r") as upload_js:
        ans = upload_js.read()
    return Response(content=ans, media_type="text/javascript")

@app.post("/backend.api/upload", summary="Upload user file. Convert mp4 to mp3 using moviepy. And returns mp3 file", tags=["upload"])
async def mp4ToMp3(background_task: BackgroundTasks, request: Request, user_agent: str | None = Header(default=None), file: UploadFile = File(...)):
    delete_file()
    client_host = request.client.host
    name_file = file.filename
    background_task.add_task(write_in_log, ip_address=client_host, user_agent=user_agent, request={"url": "/backend.api/upload", "method": "POST", "body": name_file})
    name_without_format = name_file[:len(name_file)-4]
    if name_file[-4:] != ".mp4":
        raise Unikformaterror(name=name_file[-4:])
    with open(f"unuseful_cache/{file.filename}", 'wb') as mp4_file:
        content = await file.read()
        mp4_file.write(content)
        mp4_file.close() 
    mp3(name=name_without_format)
    return FileResponse(f"unuseful_cache/{name_without_format}.mp3", filename=f"{name_without_format}.mp3", media_type="application/octet-stream")
