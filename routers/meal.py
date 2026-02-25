from fastapi import APIRouter,Depends
import schemas
from sqlalchemy.orm import Session
from database import get_db
from repositories import mealRepo
from typing import List
router=APIRouter(
    prefix="/meal",
    tags=["Meals"]
)

@router.post("/")
def create_meal(request:schemas.MealBase,db:Session=Depends(get_db)):
    return mealRepo.create(request,db)
@router.get("/{id}",response_model=schemas.MealBase)
def show_meal(id:int,db:Session=Depends(get_db)):
    return mealRepo.show(id,db)

# @router.delete("/{id}")
# def delete_meal(id:int):
#     return mealRepo.delete(id)

