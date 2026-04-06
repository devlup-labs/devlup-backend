from fastapi import FastAPI


from server.routes import application_routes
from server.routes import stats_routes

app = FastAPI()


app.include_router(application_routes.router)
app.include_router(stats_routes.router)