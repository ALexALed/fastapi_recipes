from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


# Whenever an HTTPException error is raised anywhere in your application,
# FastAPI will use this handler to return a custom response.

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": "Oops!"})

def test():
    raise HTTPException(status_code=400)
