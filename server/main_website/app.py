from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.main_website.routes import blogs
from server.main_website.routes import videos
from server.main_website.routes import podcasts
from server.main_website.routes import team
from server.main_website.routes import timeline
from server.main_website.routes import auth, admin
from server.main_website.routes import comments
from server.main_website.routes import contact

main_app = FastAPI(redirect_slashes=True) 

main_app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http?://.*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

main_app.include_router(auth.router)
main_app.include_router(admin.router)
main_app.include_router(blogs.router)
main_app.include_router(videos.router)
main_app.include_router(podcasts.router)
main_app.include_router(team.router)
main_app.include_router(timeline.router)
main_app.include_router(comments.router)
main_app.include_router(contact.router)