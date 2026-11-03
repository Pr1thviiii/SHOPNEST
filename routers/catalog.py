from fastapi import APIRouter ,Depends , HTTPException , Query
from models import ProductModel , UserModel
from schemas import AddProduct , AddRespone , UpdateRequest
from database import get_db
from auth_utilis import require_admin    
from sqlalchemy.orm import Session 
from sqlalchemy import select 

router = APIRouter(prefix="/product",tags=["Products"])


admin_error = HTTPException(
    status_code=403,
    detail="Not allowed to perform this operation"
    )

@router.post("/",response_model=AddRespone)
def add_product(userdata:AddProduct,
                db:Session=Depends(get_db),
                current_user:UserModel=Depends(require_admin)):

    
    query = select(ProductModel).where(ProductModel.product_name==userdata.product_name)
    product_ = db.scalars(query).first()

    if product_ :
        raise HTTPException(
            status_code=409,
            detail="Product already exist"
        )

    new_product = ProductModel(
        product_name = userdata.product_name,
        price = userdata.price,
        stock_count = userdata.stock_count,
        category = userdata.category,
        description = userdata.description
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.patch("/{id}",response_model=AddRespone)
def update_product(id:int,
                userdata:UpdateRequest,
                db:Session=Depends(get_db),
                current_user:UserModel=Depends(require_admin)):

    product_ = db.get(ProductModel,id)

    if product_ is None:
        raise HTTPException(
            status_code=404,
            detail="Product not exist"
        )
    if userdata.product_name is not None :
        product_.product_name = userdata.product_name

    if userdata.price is not None:
        product_.price = userdata.price

    if userdata.stock_count is not None:
        product_.stock_count = userdata.stock_count

    if userdata.category is not None :
        product_.category = userdata.category

    if userdata.description is not None :
        product_.description = userdata.description

    db.commit()
    db.refresh(product_)

    return product_

@router.get("/all",response_model=list[AddRespone])
def get_all_products(search : str | None = None ,
                     category : str | None = Query(default=None,max_length=100) ,
                     max_price : float | None = Query(default=None),
                     min_price : float | None = Query(default=None),
                     limit:int=Query(default=2,ge=1,le=20),
                     skip:int=Query(default=0,ge=0,le=1000),
                     db:Session=Depends(get_db)):

    query = select(ProductModel)

    if search:
        query = query.where(ProductModel.product_name.ilike(f"%{search}%"))

    if category:
        query = query.where(ProductModel.category == category)

    if max_price is not None:
        query = query.where(ProductModel.price <= max_price)

    if min_price is not None:
        query = query.where(ProductModel.price >= min_price)
        
       
    query = query.limit(limit).offset(skip)
    products = db.scalars(query).all()

    return products

@router.get("/{id}",response_model=AddRespone)
def get_product(id:int,
                db:Session=Depends(get_db)):

    product = db.get(ProductModel,id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not exist"
        )

    return product

@router.delete("/{id}")
def delete_product(id:int,
                   db:Session=Depends(get_db),
                   current_user:UserModel=Depends(require_admin)):

    product_ = db.get(ProductModel,id)

    if product_ is None:
        raise HTTPException(
            status_code=404,
            detail="Product not exist"
            )
    
    db.delete(product_)
    db.commit()

    return {"message":"Product deleted !"}

