import os
from dotenv import load_dotenv
load_dotenv()
from starlette.applications import Starlette
from starlette.routing import Host

from server.projects_website.app import projects_app
from server.main_website.app import main_app

app = Starlette(routes=[
    Host("projects.devluplabs.tech", app=projects_app),
    Host("devluplabs.tech", app=main_app),
    Host("devlup-labs.vercel.app", app=main_app)
])