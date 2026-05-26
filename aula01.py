"""
Coletar

"""

import os

import redis
from dotenv import load_dotenv

load_dotenv()

_HOST = os.getenv("REDIS_HOST")
_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASS = os.getenv("REDIS_PASS")

if not _HOST or not _PORT:
    raise ValueError(
        "ERRO: REDIS_HOST e REDIS_PORT precisam estar definidos no arquivo .env"
    )

REDIS_HOST: str = _HOST
REDIS_PORT: int = int(_PORT)

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    username=REDIS_USER,
    password=REDIS_PASS,
)

success = r.set("foo", "bar")
# True

result = r.get("teste")
print(result)
success = r.set("teste", "testeeee")
# >>> bar
