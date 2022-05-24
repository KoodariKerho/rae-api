import os
from models.users import UserModel
from models.users import UserBaseModel
from models.events import EventModel
from models.events import EventBaseModel


from fastapi import FastAPI, Path, Query, Body, Header, HTTPException, status
from mangum import Mangum

stage = os.environ.get('STAGE', None)
root_path = f"/{stage}" if stage else "/"

app = FastAPI(title="Rae-api-v2", root_path=root_path) # Here is the magic​


@app.get("/users/{id}", tags=["users"])
def get_user(id: str):
    user = UserModel.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/create-user/{id}")
def create_user(id: str, user: UserBaseModel):
    # Is this a new user? If so, create a new user.
    try:
        user_id = UserModel.get(id)
        if user_id:
            raise HTTPException(status_code=400, detail="User already exists")
    except:
        #Create user to a dynamodb table
        user = UserModel(id, username=user.username, photo=user.photo, email=user.email, friends=[])
        user.save()
        return {"message": "User with id ${id} created"}

@app.put("/update-user/{id}")
def update_user(id: str, userModified: UserBaseModel):
    users = UserModel.scan()
    for user in users:
        if not user.id == id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user = UserModel.get(id)
    user.username = userModified.username
    user.photo = userModified.photo
    user.email = userModified.email
    user.friends = userModified.friends
    user.save()
    return {"message": "User with id ${id} updated"}

@app.put("/add-friend/{id}/{friendId}")
def add_friend(id: str, friendId: str):
    
    user = UserModel.get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.friends.append(friendId)
    user.save()

    friend = UserModel.get(friendId)
    if not friend:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    friend.friends.append(id)
    friend.save()
    return {"message": "Friend added"}

@app.post("/add-event-attendee/{userId}/{eventId}")
def add_event_attendee(userId: str, eventId: str, event: EventBaseModel):
    try:
        event = EventModel.get(eventId)
        event.attendees.append(userId)
        event.save()
    except:
        #Create user to a dynamodb table
        event = EventModel(eventId, attendees=[userId])
        event.save()

@app.get("/event-attendees/{eventId}")
def get_event_attendees(eventId: str):
    try:
        event = EventModel.get(eventId)
        return event.attendees
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")  

@app.post("add-post/{userId}/{eventId}")
def add_post(userId: str, eventId: str):
    try:
        user = UserModel.get(userId)
        user.posts.append(eventId)
        user.save()
    except:
        #Create user to a dynamodb table
        user = UserModel(userId, posts=[eventId])
        user.save()
                 


handler = Mangum(app)