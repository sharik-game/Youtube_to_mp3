from pydantic import BaseModel
class Message(BaseModel):
    message: str

class Uncorrect_format(Exception):
    def __init__(self, name: str):
        self.name = name

class Uncorrect_cookie(Exception):
    def __init__(self, cookie: str):
        self.cookie = cookie