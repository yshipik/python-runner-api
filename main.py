from fastapi import FastAPI, Response, status, UploadFile, Form, File
from typing import Annotated
from sandbox import CodeRunner
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class CodeModel(BaseModel):
    code: str

class TestQueryModel(BaseModel):
    code: str
    filename: str

origins = ["http://localhost:3000", "http://172.17.0.1"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_methods=["POST","GET", "OPTIONS"],
    allow_headers=["*"]
)
def handle_bad_behavior(status_code, error: str, response: Response) -> bool:
    if status_code == -1:
        if "Server Error" in error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return True
        else:
            response.status_code = 200
            return False

def wrap_response(error: str, is_server_failure: bool):
    if is_server_failure:
        return { "status": "failure", "message": error}

@app.post("/api/python/run")
async def run_code(code: CodeModel, response: Response):
    status_code, output, error = CodeRunner.run_code(code.code)
    if status_code == -1:
        state = handle_bad_behavior(status_code, error, response)
        wrap_response(error, state)
    return {'status_code': code, 'output': output, 'error': error}

@app.post("/api/python/test")
async def test_code(data: TestQueryModel, response: Response):
    status_code, output, error = CodeRunner.test_code(data.code, data.filename)
    if status_code == -1:
        print(error)
        state = handle_bad_behavior(status_code, error, response)
        wrap_response(error, state)
    return {'status_code': status_code, 'output': output, 'error': error}

@app.post("/api/python/dev/test")
async def add_test(file: UploadFile, response: Response):
    data = await file.read()
    if CodeRunner.add_test_file(data, file.filename):
        return {"status": "success", 'message': "File was added"}
    response.status_code = 400
    return {"status": "failure", "message": "Can't add file"}

@app.get("/api/python/dev/test")
async def get_test(response: Response):
    files = CodeRunner.list_test_files()
    if files != None:
        return {"status": "success", "files": files}
    else:
        response.status_code = 400
        return {"status": "failure", "message": "can't give back test file"}