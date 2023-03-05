from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

@router.get("/frontend/main_site_page/main_page.js", tags=["main"])
async def read_main_js():
    with open("frontend/main_site_page/main_page.js", "r") as main_pagejs:
        ans = main_pagejs.read()
    return Response(content=ans, media_type="text/javascript")
@router.get("/frontend/main_site_page/styles.css", tags=["main"])
async def read_main_css():
    with open("frontend/main_site_page/styles.css", "r") as main_pagecss:
        ans = main_pagecss.read()
    return Response(content=ans, media_type="text/css")
@router.get("/frontend/main_site_page/red-youtube-logo-png-xl.png", tags=["main"])
async def read_first_button_png():
    with open("frontend/main_site_page/red-youtube-logo-png-xl.png", "rb") as file:
        ans = file.read()
    return Response(content=ans, media_type="image/png")
@router.get("/frontend/main_site_page/i.png", tags=["main"])
async def read_second_button_png():
    with open("frontend/main_site_page/i.png", "rb") as file:
        ans = file.read()
    return Response(content=ans, media_type="image/png")
@router.get("/frontend/upload2/styles.css", tags=["upload"])
async def read_upload_stules():
    with open("frontend/upload2/styles.css", "r") as main_styles:
        ans = main_styles.read()
    return Response(content=ans, media_type="text/css")
@router.get("/frontend/upload2/upload1.js", tags=["upload"])
async def read_upload_js():
    with open("frontend/upload2/upload1.js", "r") as upload_js:
        ans = upload_js.read()
    return Response(content=ans, media_type="text/javascript")