from fastapi import FastAPI
from database import Base , engine
from routers.auth import router as AuthRouter
from routers.catalog import router as ProductRouter
from routers.cart import router as CartRouter


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SHOPNEST")

app.include_router(AuthRouter)
app.include_router(ProductRouter)
app.include_router(CartRouter)

