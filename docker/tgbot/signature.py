from aiogram import Bot, Dispatcher
import config as cfg
from database.requests import DBUsers, DBReferrals

class MyBot:
    def __init__(self):
        self.bot = Bot(token=cfg.TOKEN)
        self.dp = Dispatcher()
        self.db_user = DBUsers()
        self.db_ref = DBReferrals()