from fastapi import FastAPI
from server.routes import auth_routes
# from server.routes import project_routes
# from server.routes import mentor_routes
# from server.routes import timeline_routes
from server.routes import application_routes
# from server.routes import stats_routes

app = FastAPI()
# app.include_router(project_routes.router)
# app.include_router(mentor_routes.router)
# app.include_router(timeline_routes.router)
app.include_router(auth_routes.router)
app.include_router(application_routes.router)
# app.include_router(stats_routes.router)