import asyncio
from fastapi import FastAPI, HTTPException
from signature import MyBot
from handlers.client import Client
from aiogram import types
import uvicorn

from proccess.check_subscribes import check_subscribes
from schemas.user import UserRequest, UserResponse


app = FastAPI()

# Создаем экземпляр бота
bot_instance = MyBot()
handlers = Client(bot_instance, bot_instance.db_user, bot_instance.db_ref)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())

async def start_bot():
    await bot_instance.dp.start_polling(bot_instance.bot)

# Эндпоинт для проверки подписки пользователя на канал
@app.get("/check_subscribe")
async def check_subscribe(request: UserRequest) -> UserResponse:
    try:
        return check_subscribes(request=request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))