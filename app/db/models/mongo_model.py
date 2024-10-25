from pydantic import BaseModel, Field
from typing import Optional

class MongoModel(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Sample Name",
                "description": "Sample Description"
            }
        }
