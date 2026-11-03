from decimal import Decimal
from database import Base
from sqlalchemy import Integer , String , Numeric , CheckConstraint , ForeignKey , UniqueConstraint
from sqlalchemy.orm import Mapped , mapped_column , relationship
from typing import Optional

class UserModel(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    name : Mapped[str] = mapped_column(String(100),nullable=False)
    email : Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    password : Mapped[str] = mapped_column(String(255),nullable=False)
    role :  Mapped[str] = mapped_column(String(100),default="customer")
    

    cart_item_info : Mapped[list["CartModel"]] = relationship(cascade="all,delete-orphan")

class ProductModel(Base):
    __tablename__ = "products"

    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    product_name : Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    price : Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    stock_count : Mapped[int] = mapped_column(Integer,nullable=False)
    category : Mapped[str] = mapped_column(String(100),nullable=False)
    description :  Mapped[Optional[str]] = mapped_column(String(500))

    __table_args__ = (
        CheckConstraint("price > 0"),
        CheckConstraint("stock_count >= 0"),
    )

class CartModel(Base):
    __tablename__ = "cart_items"

    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    product_id : Mapped[int] = mapped_column(Integer,ForeignKey("products.id",ondelete="CASCADE"))
    quantity : Mapped[int] = mapped_column(Integer,default=1)

    user_info : Mapped["UserModel"] = relationship()
    product_info : Mapped["ProductModel"] = relationship()

    __table_args__ = (
        CheckConstraint("quantity >= 1"),
        UniqueConstraint("user_id","product_id"),
    )

class OrderModel(Base):
    __tablename__ = "orders"

    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    order_id : Mapped[int] = mapped_column(Numeric(8),nullable=False,unique=True)
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    product_id : Mapped[int] = mapped_column(Integer,ForeignKey("products.id",ondelete="CASCADE"))





