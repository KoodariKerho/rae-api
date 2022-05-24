from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute, JSONAttribute
from pydantic import BaseModel
from typing import Optional

class PostModel(Model):
    """
    A DynamoDB Post
    """
    class Meta:
        table_name = 'posts'
        region = 'eu-north-1'
    id = UnicodeAttribute(hash_key=True)
    author = UnicodeAttribute()
    eventName: UnicodeAttribute()
    date: UTCDateTimeAttribute()
    availability: NumberAttribute()
    companyPicture: UnicodeAttribute()
    eventPicture: UnicodeAttribute()
    eventPlace: UnicodeAttribute()
    salesOngoing: BooleanAttribute()
    timeUntilSalesStart: NumberAttribute()
    timeUntilActual: NumberAttribute()

class PostBaseModel(BaseModel):
    """
    A BaseModel for Post
    """
    id: str
    author: str
    date: Optional[str] = None
    eventName: Optional[str] = None
    availability: Optional[bool] = None
    companyPicture: Optional[str] = None
    eventPicture: Optional[str] = None
    eventPlace: Optional[str] = None
    salesOngoing: Optional[bool] = None
    timeUntilSalesStart: Optional[int] = None
    timeUntilActual: Optional[int] = None
