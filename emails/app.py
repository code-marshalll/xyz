from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from automail import send_email

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS)
app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send-single")
def send_single(request:Request,hr_email: str = Form(...), subject: str = Form(...), role: int = Form(...)):
    success, message = send_email(hr_email, subject, role)
    return templates.TemplateResponse("index.html",{"request": request,"success": success, "message": message})

@app.get("/send-multiple", response_class=HTMLResponse)
def multiple_form(request: Request):
    return templates.TemplateResponse("send-multiple.html", {"request": request})


@app.post("/send-multiple")
def send_multiple(hr_emails: List[str] = Form(...), subject: str = Form(...), role: int = Form(...)):
    results = []
    for email in hr_emails:
        success, message = send_email(email, subject, role)
        results.append({email: message})
    return {"results": results}
