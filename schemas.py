from pydantic import BaseModel , Field , ConfigDict
from typing import Optional


class RequestRegister(BaseModel):
    name : str = Field(max_length=100)
    email : str = Field(max_length=100)
    password : str

class ResponseRegis(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name : str
    email : str

class RequestLogin(BaseModel):
    email : str = Field(max_length=100)
    password : str

class AddProduct(BaseModel):
    product_name : str = Field(max_length=100)
    price : float = Field(gt=0)
    stock_count : int = Field(ge=0)
    category : str
    description : Optional[str] = Field(max_length=500,default=None)

class AddRespone(BaseModel):
    id : int
    product_name : str
    price : float 
    stock_count : int 
    category : str
    description : Optional[str] = None

class UpdateRequest(BaseModel):
    product_name : Optional[str] = Field(default=None,max_length=100,min_length=1)
    price : Optional[float] = Field(default=None,gt=0)
    stock_count : Optional[int] = Field(default=None,ge=0)
    category : Optional[str] = Field(default=None,min_length=1)
    description : Optional[str] = Field(default=None,max_length=500)

class AddCartRequest(BaseModel):
    product_id : int
    quantity : int = Field(default=1,ge=1)

class AddCartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id : int
    product_id : int
    quantity : int

class ProductInfo(BaseModel):
    product_name : str
    model_config = ConfigDict(from_attributes=True)

class ViewCartResponse(BaseModel):
    id : int
    product_id : int
    quantity : int
    product_info : ProductInfo
    model_config = ConfigDict(from_attributes=True)

class UpdateCartRequest(BaseModel):
    quantity : int = Field(ge=1)

class CartTotalResponse(BaseModel):
    total_amount : float = Field(ge=0)
    model_config = ConfigDict(from_attributes=True)