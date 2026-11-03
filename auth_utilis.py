import os , jwt
from pwdlib import PasswordHash
from datetime import timezone , timedelta , datetime
from dotenv import load_dotenv
from fastapi import HTTPException , Depends
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from database import get_db 
from models import UserModel
from sqlalchemy.orm import Session

load_dotenv()

OAuth2 = HTTPBearer()

SECRET_KEY = os.getenv("KEY")
ALGORITHM = os.getenv("algo")
EXPIRE_TIME = os.getenv("expire")

pwd_hash = PasswordHash.recommended()

user_not_exist = HTTPException(
    status_code=404,
    detail="User not exist"
)

def Password_Hashing(password):
    return pwd_hash.hash(password)

def Password_Verify(Plain,Hashed):
    return pwd_hash.verify(Plain,Hashed)

def create_token(data:dict):
    encoded_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(EXPIRE_TIME))
    encoded_data.update({"exp" : expire})
    encoded = jwt.encode(encoded_data,SECRET_KEY,algorithm=ALGORITHM)
    return encoded

def get_current_user(credential: HTTPAuthorizationCredentials = Depends(OAuth2),
                     db:Session = Depends(get_db)):
    token = credential.credentials
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = db.get(UserModel,int(user_id))
        
        return user
     
    except:
        raise jwt.InvalidTokenError

def require_admin(current_user : UserModel = Depends(get_current_user)):
   
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not allowed to perform this operation"
        )
    return current_user

       
    
    
