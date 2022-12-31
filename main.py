import datetime
import logging
import time
from fastapi import BackgroundTasks, FastAPI, File, Header, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from mp4_to_mp3 import mp3
from files_del import delete_file
from description import OpenAPI_desc
logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s %(asctime)s %(message)s")
app = FastAPI(
    title="YoTube to mp3 online converter",
    description=OpenAPI_desc.description,
    version="0.1"
)

def write_in_log(ip_address: str, user_agent, request: dict):
    date_now = datetime.datetime.now()
    date_now_str: str = date_now.strftime('%m/%d/%y %H:%M:%S')
    url: str = request["url"]
    method: str = request["method"]
    body = request["body"]
    with open("log.txt", "a") as log_file:
        log_file.write(f"Url: {url}, Method: {method}, IP: {ip_address}, User-Agent: {user_agent}, Date: {date_now_str}, Body: {body}\n")
    logging.info("Writing ещ logs was successful")
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
async def main_window(request: Request, background_tasks: BackgroundTasks, user_agent: str | None = Header(default=None)):
    client_host = request.client.host
    background_tasks.add_task(write_in_log, ip_address=client_host, user_agent=user_agent, request={"url": "/", "method": "GET", "body": None})
    with open("frontend/index.html", "r") as file:
        answer = file.read()
    return HTMLResponse(answer)


@app.post("/backend.api/upload")
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
