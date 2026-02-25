from fastapi import APIRouter,Depends
import schemas
from sqlalchemy.orm import Session
from database import get_db
from repositories import botRepo
from typing import List
router=APIRouter(
    prefix="/bot",
    tags=["Gluco Bot"]
)

################## Conversations ##################

@router.post("/conversation")
def create_conversation(request:schemas.ConversationBase,db:Session=Depends(get_db)):
    return botRepo.create(request,db)

@router.get("/conversation/{id}",response_model=schemas.ConversationShow)
def show_conversation(id:int,db:Session=Depends(get_db)):
    return botRepo.show(id,db)

@router.get("/conversation/all/{user_id}",response_model=List[schemas.ConversationAll])
def all_conversations(user_id:int,db:Session=Depends(get_db)):
    return botRepo.get_all(user_id,db)

@router.delete("/conversation/{id}")
def delete_conversation(id:int,db:Session=Depends(get_db)):
    botRepo.delete(id,db)
    return {"message": f"Analyse {id} deleted successfully!"}



################## Messages ##################

@router.post("/message")
def create_message(request:schemas.MessageBase,db:Session=Depends(get_db)):
    return botRepo.create_message(request,db)

# @router.get("/message/{id}",response_model=schemas.MessageShow)
# def show_message(id:int,db:Session=Depends(get_db)):
#     return botRepo.show(id,db)

@router.get("/message/all/{conv_id}",response_model=List[schemas.MessageShow])
def all_messages(conv_id:int,db:Session=Depends(get_db)):
    return botRepo.get_messages(conv_id,db)


