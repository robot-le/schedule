from typing import Annotated
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator


PyObjectId = Annotated[str, BeforeValidator(str)]

class Schedule(BaseModel):
    id: PyObjectId | None = Field(alias='_id', default=None)
    person: str
    subject: str
    date_start: datetime = Field(default=datetime.today())
    date_finish: datetime = Field(default=datetime.today() + timedelta(days=10))
    model_config = ConfigDict(populate_by_name=True)

class ScheduleCollection(BaseModel):
    schedules: list[Schedule]