from pydantic import BaseModel


class ProjectMentorModel(BaseModel):

    project_id: str
    mentor_id: str