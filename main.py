import os
from models.users import UserModel
from models.users import UserBaseModel


from fastapi import FastAPI, Path, Query, Body, Header, HTTPException, status
from mangum import Mangum
stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(title="MyAwesomeApp", openapi_prefix=openapi_prefix) # Here is the magic​



@app.post("/create-user/{id}")
def create_user(id: str, user: UserBaseModel):
    # Is this a new user? If so, create a new user.
    users = UserModel.scan()
    for user in users:
        if user.id == id:
            raise HTTPException(status_code=400, detail="User already exists")
    #Create user to a dynamodb table
    user = UserModel(id, username=user.username, photo=user.photo, email=user.email)
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
    user.save()
    return {"message": "User with id ${id} updated"}

handler = Mangum(app)