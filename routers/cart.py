from fastapi import APIRouter ,  Depends , HTTPException
from database import get_db
from auth_utilis import get_current_user
from sqlalchemy.orm import Session 
from sqlalchemy import select
from schemas import AddCartRequest , AddCartResponse,ViewCartResponse,UpdateCartRequest,CartTotalResponse
from models import ProductModel , UserModel , CartModel

router = APIRouter(prefix="/cart",tags=["Cart"])

@router.post("/",response_model=AddCartResponse,status_code=201)
def add_cart(userdata:AddCartRequest,
             db:Session=Depends(get_db),
            current_user:UserModel=Depends(get_current_user)
            ):

    product = db.get(ProductModel,userdata.product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not exist"
        )
    
    query = select(CartModel).where(CartModel.user_id == current_user.id,
                                    CartModel.product_id == userdata.product_id)
    existing_item = db.scalars(query).first()

    quantity = existing_item.quantity if existing_item  else 0   
    final_quantity = quantity + userdata.quantity

    if final_quantity > product.stock_count:
        raise HTTPException(
            status_code=400,
            detail="not enough stock"
        )

    if existing_item:
        existing_item.quantity = final_quantity
        item = existing_item 

    else:            
        item = CartModel(
                user_id = current_user.id,
                product_id = userdata.product_id,
                quantity = final_quantity
                )
        db.add(item)

    db.commit()
    db.refresh(item)

    return item

@router.get("/",response_model=list[ViewCartResponse])
def view_cart(db:Session=Depends(get_db),
              current_user:UserModel=Depends(get_current_user)):

    
    query = select(CartModel).where(CartModel.user_id == current_user.id)
    query = query.order_by(CartModel.id)
    cart_items = db.scalars(query).all()


    return cart_items

@router.patch("/{product_id}",response_model=ViewCartResponse,status_code=200)
def update_cart(product_id:int,
                userdata : UpdateCartRequest,
                db:Session=Depends(get_db),
                current_user:UserModel=Depends(get_current_user)):

    product = db.get(ProductModel,product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not exist"
        )

    query = select(CartModel).where(CartModel.product_id == product_id,
                                    CartModel.user_id==current_user.id)

    cart_product  = db.scalars(query).first()

    if cart_product is None:
        raise HTTPException(
            status_code=404,
            detail="item not in cart"
        )   
    if userdata.quantity > product.stock_count :
        raise HTTPException(
            status_code=400,
            detail="Quantity exceed the stock quantity"
        )

    
    cart_product.quantity = userdata.quantity

    db.commit()
    db.refresh(cart_product)

    return cart_product

@router.delete("/",status_code=204)  
def clear_cart(db:Session=Depends(get_db),
                current_user:UserModel=Depends(get_current_user)):

    query = select(CartModel).where(CartModel.user_id==current_user.id)
    cart_items = db.scalars(query).all()

    for i in cart_items:
        db.delete(i)

    db.commit()

@router.delete("/{product_id}")
def delete_product(product_id:int,
                db:Session=Depends(get_db),
                current_user:UserModel=Depends(get_current_user)):

    query = select(CartModel).where(CartModel.product_id==product_id,
                                    CartModel.user_id==current_user.id)
    cart_item = db.scalars(query).first()

    if cart_item is None:
        raise HTTPException(
            status_code=404,
            detail="item not in cart"
        )

    db.delete(cart_item)
    db.commit()
    return {"message":"deleted successfully"}

@router.get("/total",response_model=CartTotalResponse)
def get_total_amount(db:Session=Depends(get_db),
                 current_user:UserModel=Depends(get_current_user)):

    query = select(CartModel).where(CartModel.user_id==current_user.id)
    cart_rows = db.scalars(query).all()

    total_amount = 0

    for row in cart_rows:
        subtotal = (row.quantity * row.product_info.price)
        total_amount += subtotal

    return {"total_amount": round(total_amount,2)}




