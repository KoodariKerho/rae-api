from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute, JSONAttribute
from pydantic import BaseModel
from typing import Optional

class EventModel(Model):
    """
    A DynamoDB Event
    """
    class Meta:
        table_name = 'events'
        region = 'eu-north-1'
    event_id = UnicodeAttribute(hash_key=True)
    attendees = ListAttribute()

class EventBaseModel(BaseModel):
    """
    A BaseModel for Event
    """
    event_id: str
    attendees: Optional[list] = None

class EventListModel(BaseModel):
    model: list