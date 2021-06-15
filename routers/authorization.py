from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from starlette.requests import empty_receive

auth = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.post("/token")
def access_token_generator(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"user": form_data.username}
