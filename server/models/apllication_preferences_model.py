from pydantic import BaseModel


class ApplicationPreferenceModel(BaseModel):

    preference_id: str

    application_id: str
    project_id: str

    proposal: str
    project_interest: str

    priority: int