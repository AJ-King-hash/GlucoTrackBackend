from fastapi import APIRouter
from StartingPackages import *
from repositories import userRepo
router=APIRouter(
prefix="/user",
tags=["Users"],

)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUserWithMessage)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return {"message": "User Created successfully ", "user": userRepo.create(request,db)}   

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

