from StartingPackages import *
from fastapi import APIRouter
from JwtToken import timedelta,ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from repositories.authRepo import *

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login",response_model=schemas.Token)
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    # 1-check the user
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not Hash.verify(request.password,user.password):
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    #2- Generate JWT token and return it     
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # return user
    return schemas.Token(access_token=access_token, token_type="bearer")



