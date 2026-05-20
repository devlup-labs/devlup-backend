from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes import auth_routes
from server.routes import project_routes
from server.routes import mentor_routes
from server.routes import timeline_routes
from server.routes import application_routes
from server.routes import stats_routes
from server.routes import form_field_routes
from server.routes import google_auth_routes
from server.routes import mentor_panel_routes
from server.routes import results_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(project_routes.router)
app.include_router(mentor_routes.router)
app.include_router(timeline_routes.router)
app.include_router(auth_routes.router)
app.include_router(application_routes.router)
app.include_router(stats_routes.router)
app.include_router(form_field_routes.router)
app.include_router(google_auth_routes.router)
app.include_router(mentor_panel_routes.router)
app.include_router(results_routes.router)