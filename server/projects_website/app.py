from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.projects_website.routes import auth_routes
from server.projects_website.routes import project_routes
from server.projects_website.routes import mentor_routes
from server.projects_website.routes import timeline_routes
from server.projects_website.routes import application_routes
from server.projects_website.routes import stats_routes
from server.projects_website.routes import form_field_routes
from server.projects_website.routes import google_auth_routes
from server.projects_website.routes import mentor_panel_routes
from server.projects_website.routes import results_routes

projects_app = FastAPI()

projects_app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
projects_app.include_router(project_routes.router)
projects_app.include_router(mentor_routes.router)
projects_app.include_router(timeline_routes.router)
projects_app.include_router(auth_routes.router)
projects_app.include_router(application_routes.router)
projects_app.include_router(stats_routes.router)
projects_app.include_router(form_field_routes.router)
projects_app.include_router(google_auth_routes.router)
projects_app.include_router(mentor_panel_routes.router)
projects_app.include_router(results_routes.router)