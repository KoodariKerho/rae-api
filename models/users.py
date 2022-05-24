from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute
from pydantic import BaseModel
from typing import Optional

class UserModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = 'users'
        region = 'eu-north-1'
    id = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()
    username = UnicodeAttribute()
    photo = UnicodeAttribute()
    friends = ListAttribute()

class UserBaseModel(BaseModel):
    """
    A BaseModel for User
    """
    id: str
    email: str
    username: Optional[str] = None
    photo: Optional[str] = None
    friends: Optional[list] = None
