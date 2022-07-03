from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/asd")
async def asd():
    return HTMLResponse("<h1>Hi :D</h1>", status_code=200)


import uvicorn

uvicorn.run(app, host="127.0.0.1", port=3000)
