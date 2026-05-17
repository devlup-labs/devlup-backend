from pydantic import Field, ConfigDict
from datetime import datetime, timezone
from typing import Optional, Any
from bson import ObjectId
from server.projects_website.schemas.project_schema import ProjectBase

try:
    from pydantic_core import core_schema
    PYDANTIC_V2 = True
except ImportError:
    PYDANTIC_V2 = False

if PYDANTIC_V2:
    class PyObjectId(str):
        @classmethod
        def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: Any,
        ) -> core_schema.CoreSchema:
            return core_schema.json_or_python_schema(
                json_schema=core_schema.str_schema(),
                python_schema=core_schema.union_schema([
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema([
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(cls.validate),
                    ])
                ]),
                serialization=core_schema.plain_serializer_function_ser_schema(
                    lambda x: str(x)
                ),
            )

        @classmethod
        def validate(cls, value) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)
else:
    class PyObjectId(ObjectId):
        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def validate(cls, v):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return ObjectId(v)

        @classmethod
        def __modify_schema__(cls, field_schema):
            field_schema.update(type="string")


class ProjectModel(ProjectBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    if PYDANTIC_V2:
        model_config = ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True,
            json_encoders={ObjectId: str}
        )
    else:
        class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            json_encoders = {ObjectId: str}