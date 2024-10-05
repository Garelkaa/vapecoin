import asyncio
from signature import MyBot
from handlers.client import Client

async def start():
    bot_instance = MyBot()
    handlers = Client(bot_instance, bot_instance.db_user, bot_instance.db_ref)
    await bot_instance.dp.start_polling(bot_instance.bot)

if __name__ == '__main__':
    asyncio.run(start())
