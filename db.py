import redis
from typing import Literal


class Redis_endpoints:
    def __init__(self, host: str = 'redis', port: int = 6379, db: int = 0, decode_response: Literal[True] = True):
        # pool = redis.ConnectionPool(host=host, port=port, db=db)
        r = redis.Redis(host=host, port=port)
        self.r = r
    def set_value(self, key: str, value: str) -> bool | None:
        return self.r.set(key, value) 

    def get_value(self, key) -> bytes | None:
        return self.r.get(key)
