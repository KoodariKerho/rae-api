import os
from models.users import UserModel
from models.users import UserBaseModel
from models.events import EventModel
from models.events import EventBaseModel
from models.events import EventListModel
import logging
from urllib.request import urlopen
import json



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
        if user_id.id == id:
            raise HTTPException(status_code=409, detail="User already exists")
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
    user.posts = userModified.posts
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

@app.post("/add-event-attendee-and-post-to-user/{userId}/{eventId}")
def add_event_attendee(userId: str, eventId: str, event: EventBaseModel):
    try:
        event = EventModel.get(eventId)
        event.attendees.append(userId)
        event.save()
    except:
        #Create user to a dynamodb table
        event = EventModel(eventId, attendees=[userId])
        event.save()
        #TODO: Add post to user, make it work
    try:
        print("Adding post to user")
        try:
            user = UserModel.get(userId)
            user.posts.append(eventId)
        except Exception as e:
            print(e)
            logging.error(e)
            user.posts = [eventId]
            user.save()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.get("/event-attendees/{eventId}")
def get_event_attendees(eventId: str):
    try:
        event = EventModel.get(eventId)
        return event.attendees
    except:
        return [] 
@app.get("/friends/{userId}")
def get_friends(userId: str):
    try:
        user = UserModel.get(userId)
        return user.friends
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

@app.get("/friends-events/{userId}")
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
                    events.append({"event": event, "userId": post["userId"]})
        return events
    except:
        return []





@app.get("/events")
def get_all_events():
    url = 'https://api.kide.app/api/products?city=Helsinki'
    response = urlopen(url)
    data_json = json.loads(response.read())
    items = (data_json)
    return items.get('model')


    
    

handler = Mangum(app)