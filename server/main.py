from fastapi import FastAPI, Request
from starlette.responses import Response
from main_website.app import main_app
from projects_website.app import projects_app

app = FastAPI()

@app.middleware("http")
async def dispatch_by_subdomain(request: Request, call_next):
    host = request.headers.get("host", "").lower()
    
    if "projects.abc.tech" in host:
        await projects_app.asgi_app(request.scope, request.receive, request.send)
        return Response(content=b"")
    
    else:
        await main_app.asgi_app(request.scope, request.receive, request.send)
        return Response(content=b"")