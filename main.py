import os
from models.users import UserModel
from models.users import UserBaseModel
from models.events import EventModel
from models.events import EventBaseModel
from models.users import EventUserBaseModel
import logging
from urllib.request import urlopen
import json
import boto3
from fastapi.middleware.cors import CORSMiddleware



from fastapi import FastAPI, File, UploadFile, Path, Query, Body, Header, HTTPException, status
from mangum import Mangum

stage = os.environ.get('STAGE', None)
root_path = f"/{stage}" if stage else "/"

app = FastAPI(title="Rae-api-v2", root_path=root_path) # Here is the magic​

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://hlw2l5zrpk.execute-api.eu-north-1.amazonaws.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users/{id}", tags=["users"])
def get_user(id: str):
    user = UserModel.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/create-user/{id}", tags=["users"])
def create_user(id: str, user: UserBaseModel):

    # Is this a new user? If so, create a new user.
    try:
        user_id = UserModel.get(id)
        print(user_id)
        print(id)
        if user_id.id == id:
            return "User already exists"
    except:
        #Create user to a dynamodb table
        logging.info(f"Creating user {id}")
        try:
            user = UserModel(id, username=user.username, photo=user.photo, email=user.email, friends=user.friends, posts=user.posts)
            user.save()
            return {"message": "User with id ${id} created"}
        except Exception as e:
            logging.error(e)
            print(e)
            raise HTTPException(status_code=500, detail="Error creating user")
        

@app.put("/update-user/{id}", tags=["users"])
def update_user(id: str, userModified: UserBaseModel):
    user = UserModel.get(id)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.username = userModified.username
    user.photo = userModified.photo
    user.email = userModified.email
    user.friends = userModified.friends
    user.posts = userModified.posts
    user.save()
    return HTTPException(status_code=200, detail="User updated")


@app.put("/add-friend/{id}/{friendId}", tags=["friends"])
def add_friend(id: str, friendId: str):
    
    user = UserModel.get(id)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if(friendId in user.friends):
        return HTTPException(status_code=418, detail="Friend already added")
    user.friends.append(friendId)
    user.save()

    friend = UserModel.get(friendId)
    if not friend:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    friend.friends.append(id)
    friend.save()
    return {"message": "Friend added"}

def add_to_user_posts(userId, eventId):
    user = UserModel.get(userId)
    if eventId not in user.posts:
        user.posts.append(eventId)
        user.save()
    else:
        return "Event already added"


def add_user_to_event(eventId, user: EventUserBaseModel):
    try:
        event = EventModel.get(eventId)
    except:
        event = EventModel(eventId, attendees = [], interested = [])
        event.save()
    for attendee in event.attendees:
        if attendee['userId'] == user.userId:
            return True
    event.attendees.append({"userId": user.userId, "photo": user.photo, "username": user.username})
    event.save()

@app.post("/add-post-to-user/{userId}/{eventId}", tags=["events"])
def add_event_attendee(userId: str, user: EventUserBaseModel, eventId: str):
    add_to_user_posts(userId, eventId)
    isAlready = add_user_to_event(eventId, user)
    if isAlready:
        return HTTPException(status_code=400, detail="User already added to event")
    else:
        return HTTPException(status_code=200, detail="User added to event") 

@app.get("/friends/{userId}", tags=["friends"])
def get_friends(userId: str):
    try:
        user = UserModel.get(userId)
        # Get all friend objects
        friends = []
        for friend in user.friends:
            friend = UserModel.get(friend)
            friends.append(friend)
        return friends
    except:
        return []

def get_friends_posts(user): 
    event_ids = []
    for friend in user.friends:
        try:
            friend = UserModel.get(friend)
            for post in friend.posts:
                event_ids.append({"eventId": post, "userId": friend.id})

        except:
            return "no posts"
    return event_ids

@app.get("/friends-events/{userId}", tags=["events"])
def get_friends_events(userId: str):
    user = UserModel.get(userId)
    posts = get_friends_posts(user)
    print(posts)
    all_events = get_all_events()
    events = []

    try:
        for event in all_events:
            for post in posts:
                if event["id"] in post["eventId"]:
                    friend = UserModel.get(post["userId"])
                    events.append({"event": event, "user": friend})
        return events
    except:
        return []

@app.get("/events", tags=["events"])
def get_all_events():
    url = 'https://api.kide.app/api/products?city=Helsinki'
    response = urlopen(url)
    data_json = json.loads(response.read())
    items = (data_json)
    return items.get('model')

@app.get("/event_attendees_and_interested/{eventId}", tags=["events"])
def get_event_attendees(eventId: str):
    event = EventModel.get(eventId)
    total_attendees =  len(event.attendees)
    total_intrested = len(event.interested)
    return {"total_attendees": total_attendees, "total_intrested": total_intrested}

@app.post("/event_interested/{eventId}", tags=["events"])
def get_interested(eventId: str, user: EventUserBaseModel):
    try:
        event = EventModel.get(eventId)
    except:
        event = EventModel(eventId, attendees = [], interested = [])
    try:
        for interested in event.interested:
            if interested['userId'] == user.userId:
                return HTTPException(status_code=400, detail="User already added")
    except TypeError: 
        event.interested = []
    event.interested.append({"userId": user.userId, "photo": user.photo, "username": user.username})
    event.save()
    return HTTPException(status_code=200, detail="User added")
    


handler = Mangum(app)