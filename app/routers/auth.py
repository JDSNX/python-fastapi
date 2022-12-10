from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, oauth2, schemas, models, utils

router = APIRouter(prefix="/login", tags=['Authentication'])

@router.post("/", response_model=schemas.Token)
async def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == creds.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid credentials")

    if not utils.verify(creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}