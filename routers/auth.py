from fastapi import Depends , HTTPException , APIRouter
from models import UserModel
from schemas import RequestRegister , ResponseRegis , RequestLogin
from database import get_db
from auth_utilis import  Password_Hashing , Password_Verify , create_token , require_admin
from sqlalchemy.orm import Session
from sqlalchemy import select


router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=ResponseRegis)
def UserRegister(userdata : RequestRegister,
            db:Session = Depends(get_db)
             ):
    
    query = select(UserModel).where(UserModel.email == userdata.email)
    exisiting = db.scalars(query).first()

    if exisiting:
        raise HTTPException(
            status_code=409,
            detail = "User Already exist"
        )

    Password = Password_Hashing(userdata.password)
    
    new_user = UserModel(
        name = userdata.name,
        email = userdata.email,
        password = Password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def Userlogin(userdata: RequestLogin ,
              db:Session = Depends(get_db)
              ):

    query = select(UserModel).where(UserModel.email == userdata.email)
    user = db.scalars(query).first()

    if user is None or not Password_Verify(userdata.password,user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    data_pack = {
        "sub" : str(user.id)
    }

    token = create_token(data=data_pack)
    return {
        "token" : token,
        "token_type" : "Bearer"
    }

@router.patch("/make_admin/{id}")
def make_admin(id:int,db:Session=Depends(get_db),
               current_user:UserModel=Depends(require_admin)):

    user = db.get(UserModel,id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.role == "admin":
        return {"message":f"{user.name} is already an admin !"}
    
    else:
        user.role = "admin"
        db.commit()
        return {"message":f"{user.name} is now admin !"}
    