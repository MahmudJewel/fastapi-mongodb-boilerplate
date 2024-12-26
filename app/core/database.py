from fastapi import APIRouter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import logging

from app.core.settings import MONGODB_URL, ClUSTER_NAME
from app.models import user as UserModel

logger = logging.getLogger(__name__)

db_module = APIRouter()
async def init():
    # client = AsyncIOMotorClient("mongodb+srv://mahmud:<password>@cluster0.5iguurt.mongodb.net/?appName=Cluster0")
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client.get_database(ClUSTER_NAME)
    logger.info(f"=====> DB connected : {MONGODB_URL}")
    await init_beanie(database, document_models=[UserModel.User])

@db_module.on_event("startup")
async def on_startup():
    await init()

# from fastapi import FastAPI
# from contextlib import asynccontextmanager
# from app.core.database import init

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup logic
#     await init()
#     yield  # The application runs between this line and the next
#     # Shutdown logic (if any)
#     # Example: await cleanup()

# app = FastAPI(lifespan=lifespan)


# uri = MONGODB_URL
# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# db = client.ProductionKit
# user_collection = db["users"]

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("You have successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
#     print("============> Please check your MongoDB connection.")