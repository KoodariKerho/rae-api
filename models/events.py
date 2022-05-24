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
    availability: NumberAttribute()
    companyMediaFilename: UnicodeAttribute()
    companyName: UnicodeAttribute()
    dateActualFrom: UTCDateTimeAttribute()
    dateActualUntil:UTCDateTimeAttribute()
    dateCreated: UTCDateTimeAttribute()
    datePublishFrom:UTCDateTimeAttribute()
    dateSalesFrom: UTCDateTimeAttribute()
    dateSalesUntil: UTCDateTimeAttribute()
    favoritedTimes: NumberAttribute()
    hasFreeInventoryItems: BooleanAttribute()
    hasInventoryItems: BooleanAttribute()
    isActual: BooleanAttribute()
    maxPrice: MapAttribute()
    mediaFilename: UnicodeAttribute()
    minPrice: MapAttribute()
    name: UnicodeAttribute()
    place: UnicodeAttribute()
    pricingInformation: UnicodeAttribute()
    productType: NumberAttribute()
    salesEnded: BooleanAttribute()
    salesOngoing: BooleanAttribute()
    salesPaused: BooleanAttribute()
    salesStarted: BooleanAttribute()
    timeUntilActual: NumberAttribute()
    timeUntilSalesStart: NumberAttribute()
    photoUrl: UnicodeAttribute()

class EventBaseModel(BaseModel):
    """
    A BaseModel for Event
    """
    event_id: str
    attendees: Optional[list] = None
    availability: Optional[int] = None
    companyMediaFilename: Optional[str] = None
    companyName: Optional[str] = None
    dateActualFrom: Optional[str] = None
    dateActualUntil: Optional[str] = None
    dateCreated: Optional[str] = None
    datePublishFrom: Optional[str] = None
    dateSalesFrom: Optional[str] = None
    dateSalesUntil: Optional[str] = None
    favoritedTimes: Optional[int] = None
    hasFreeInventoryItems: Optional[bool] = None
    hasInventoryItems: Optional[bool] = None
    isActual: Optional[bool] = None
    maxPrice: Optional[dict] = None
    mediaFilename: Optional[str] = None
    minPrice: Optional[dict] = None
    name: Optional[str] = None
    place: Optional[str] = None
    pricingInformation: Optional[str] = None
    productType: Optional[int] = None
    salesEnded: Optional[bool] = None
    salesOngoing: Optional[bool] = None
    salesPaused: Optional[bool] = None
    salesStarted: Optional[bool] = None
    timeUntilActual: Optional[int] = None
    timeUntilSalesStart: Optional[int] = None
    photoUrl: Optional[str] = None