from fastapi import APIRouter
from StartingPackages import *
from repositories import userRepo
from JwtToken import timedelta,ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token
router=APIRouter(
prefix="/user",
tags=["Users"],

)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUserWithMessageToken)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user=userRepo.create(request,db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"message": "User Created successfully ", "user": user,"token":schemas.Token(access_token=access_token,token_type="bearer")}   

@router.get("/{id}",response_model=schemas.ShowUserWithMessage)
def get_user(id:int,db:Session=Depends(get_db)):
    return {"message": "User has successfully Found!", "user": userRepo.show(id,db)}

@router.put("/{id}",response_model=schemas.ShowUserWithMessage)
def update_user(id:int,request:schemas.User,db:Session=Depends(get_db)):
    return {"message": "User updated successfully", "user": userRepo.update(id,request,db)}


@router.delete("/{id}")
def delete_user(id:int,db:Session=Depends(get_db)):
    userRepo.delete(id,db)
    return {"message": f"User {id} deleted successfully!"}

