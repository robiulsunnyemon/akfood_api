from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import db
from app.auth.routers import router as auth_router
from app.category.routers import router as category_router
from app.product.routers import router as product_router
from app.user.routers import router as user_router
from app.party_menu.routers import router as party_menu_router
from app.cart.routers import router as cart_router
from app.delivery_area.routers import router as delivery_area_router
from app.delivery_fee.routers import router as delivery_fee_router
from app.order.routers import router as order_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Connecting to Prisma Database...")
    await db.connect()
    yield
    # Shutdown
    logger.info("Disconnecting from Prisma Database...")
    await db.disconnect()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(party_menu_router)
app.include_router(cart_router)
app.include_router(delivery_area_router)
app.include_router(delivery_fee_router)
app.include_router(order_router)

@app.get("/")
def read_root():
    return {"message": "Server is running"}
