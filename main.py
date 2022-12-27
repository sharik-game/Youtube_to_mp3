from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from mp4_to_mp3 import mp3
from files_del import delete_file

app = FastAPI()

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
    with open(file.filename, 'wb') as mp4_file:
        content = await file.read()
        mp4_file.write(content)
        mp4_file.close() 
    name_file = file.filename
    mp3(name=name_file[len(name_file)-4:])
