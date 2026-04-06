from pydantic import BaseModel 


class Mentor(BaseModel):
    name: str
    github: str
    email: str
    description: str
    linkedin: str
    image: str
    role: str
    year: int
    