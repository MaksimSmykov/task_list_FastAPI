from fastapi import FastAPI, Request
from app.routers import task
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

app = FastAPI(swagger_ui_parameters={'tryItOutEnabled': True}, debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(task.router)

@app.get('/', response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})