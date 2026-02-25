from fastapi import APIRouter,Depends,status
import schemas
from sqlalchemy.orm import Session
from database import get_db
from repositories import riskRepo
from typing import List
router=APIRouter(
    prefix="/risk",
    tags=["Risk Factors"]
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowRiskFactorWithMessage)
def create_risk(request: schemas.RiskBase, db: Session = Depends(get_db)):
    return riskRepo.create(request,db)

@router.get("/{id}",response_model=schemas.RiskShow)
def get_risk(id:int,db:Session=Depends(get_db)):
    return riskRepo.show(id,db)

@router.put("/{id}",response_model=schemas.RiskShow)
def update_risk(id:int,request:schemas.RiskBase,db:Session=Depends(get_db)):
    return {"message": "Risk updated successfully", "user": riskRepo.update(id,request,db)}

@router.delete("/{id}")
def delete_risk(id:int,db:Session=Depends(get_db)):
    riskRepo.delete(id,db)
    return {"message": f"Risk {id} deleted successfully!"}

