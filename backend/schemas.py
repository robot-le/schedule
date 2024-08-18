from typing import Annotated
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator


PyObjectId = Annotated[str, BeforeValidator(str)]

class Schedule(BaseModel):
    id: PyObjectId | None = Field(alias='_id', default=None)
    person: str
    subject: str
    start_day: int
    end_day: int
    model_config = ConfigDict(populate_by_name=True)

class ScheduleCollection(BaseModel):
    schedules: list[Schedule]