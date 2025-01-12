from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from typing import Dict
import time
app = FastAPI()


class AdvanceMiddleWare(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def logging(self, request):
        print(f"Request: {request.method} {request.url}")

    async def log(self, path):
        print(f"Path: {path}")

    async def dispatch(self, request: Request, call_next):
       await self.logging(request)
       client_ip = request.client.host
       current_time = time.time()
       if current_time - self.rate_limit_records[client_ip] < 1:
           return Response("Too many requests", status_code=429)

       self.rate_limit_records[client_ip] = current_time
       path = request.url.path
       self.log(path)

       # process the request
       start_time = time.time()
       response = await call_next(request)
       process_time = time.time() - start_time

       custom_headers = {"X-Process-Time": str(process_time)}
       for header, value in custom_headers.items():
           response.headers.append(header, value)

       await self.log(f"Path: {path} Process Time: {process_time}")
       return response

app.add_middleware(AdvanceMiddleWare)
# @app.middleware("http")
# async def add_random_header(request, call_next):
#     '''call_next is a function that will receive the request and return a response.'''
#     print("Middleware: before request")
#     response = await call_next(request)
#     response.headers["X-Random"] = "".join(random.choices(string.ascii_letters, k=10))
#     return response

# @app.middleware("http")
# async def add_random_header2(request, call_next):
#     '''call_next is a function that will receive the request and return a response.'''
#     print("Middleware2: before request")
#     response = await call_next(request)
#     response.headers["X-Random2"] = "".join(random.choices(string.ascii_letters, k=10))
#     return response
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/test")
def read_test():
    return {"Hello": "Test"}
