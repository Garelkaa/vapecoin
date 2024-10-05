import logging
import os
import time
from aiogram import types
from aiogram.filters import CommandStart, CommandObject
import aiohttp

from signature import MyBot
from keyboards import client_kb as nav

logging.basicConfig(level=logging.INFO)

class Client:
    def __init__(self, bot_instance: MyBot, db_user, db_ref):
        self.bot = bot_instance.bot
        self.dp = bot_instance.dp
        self.db_user = db_user  # Initialize db_user
        self.db_ref = db_ref    # Initialize db_ref
        self.register_handlers()

    def register_handlers(self):
        self.dp.message(CommandStart())(self.start)

    async def start(self, message: types.Message, command: CommandObject):
        """
        Обработчик команды /start
        """
        command_args = command.args if command else None
        username = message.from_user.username if message.from_user.username else message.from_user.first_name
        
        try:
            if command_args:
                await self.process_referral(message, command_args, username)
            else:
                await self.process_registration(message, username)
        except Exception as e:
            logging.error(f"Error in start command: {e}")

    async def process_referral(self, message: types.Message, command_args: str, username: str):
    # Проверяем, существует ли пользователь
        ref_user_id = await self.db_user.find_user(message.from_user.id)
        
        if ref_user_id is None:
            # Если пользователь не существует, добавляем его
            await self.db_user.add_user(user_id=message.from_user.id, username_tg=username, password='123')
            ref_user_id = await self.db_user.find_user(message.from_user.id)
            await self.download_avatar(message.from_user.id)
            
            # Находим реферального пользователя (того, кто пригласил)
            ref_user_refferer = await self.db_user.find_user(int(command_args))
            
            if ref_user_id and ref_user_refferer:
                # Добавляем нового пользователя в реферальную систему
                await self.db_ref.add_user(
                    user_id_id=ref_user_id,
                    ref_link=f'https://t.me/vapecoins_bot?start={message.from_user.id}',
                    ref_user_id=ref_user_refferer
                )
                
                # Проверяем количество друзей, которых привел реферальный пользователь
                referral_count = await self.db_ref.get_referral_count(ref_user_refferer)
                
                # Определяем награду в зависимости от количества рефералов
                if referral_count < 3:
                    reward = 5000
                elif 4 <= referral_count <= 10:
                    reward = 7500
                else:
                    reward = 10000
                
                # Проверяем, есть ли у реферального пользователя премиум
                
                
                if message.from_user.is_premium:
                    reward *= 2  # Если премиум, удваиваем награду
                
                # Добавляем монеты новому пользователю и рефереру
                await self.db_user.increase_user_money(user_id=ref_user_id, amount=reward)
                await self.db_user.increase_user_money(user_id=ref_user_refferer, amount=reward)
                
                # Уведомляем реферального пользователя о регистрации нового пользователя
                await self.bot.send_message(command_args, f"По вашей реферальной ссылке успешно зарегистрировался @{username}. Вы получили {reward} монет!")
            
            else:
                await message.reply("Ошибка при обработке реферальной ссылки.")
        
        # Приветственное сообщение для нового пользователя
        await self.bot.send_message(
            message.from_user.id, 
            f"""Привет, {message.from_user.username}! Это VapeCoin 👋

    Жми на кнопку и смотри, как растёт твой баланс.

    Друзья есть? Зови их в игру. Так вы вместе получите ещё больше монет.

    VapeCoin - он есть, он будет всегда!""", 
            reply_markup=nav.start(message.from_user.id)
        )

    async def process_registration(self, message: types.Message, username: str):
    # Проверяем, существует ли пользователь
        ref_user_id = await self.db_user.find_user(message.from_user.id)
        
        if ref_user_id is None:
            # Если пользователь не существует, добавляем его
            await self.db_user.add_user(user_id=message.from_user.id, username_tg=username,password='123')
            ref_user_id = await self.db_user.find_user(message.from_user.id)
            
            await self.download_avatar(message.from_user.id)
        
        # Находим реферального пользователя (если это необходимо)
            ref_user_refferer = await self.db_user.find_user(123)  # Adjust the referrer ID as needed

            await self.db_ref.add_user(
                user_id_id=ref_user_id,
                ref_link=f'https://t.me/vapecoins_bot?start={message.from_user.id}',
                ref_user_id=ref_user_refferer
            )
        
        await self.bot.send_message(message.from_user.id, f"""Привет, {message.from_user.username}! Это VapeCoin 👋

Жми на кнопку и смотри, как растёт твой баланс.

Друзья есть? Зови их в игру. Так вы вместе получите ещё больше монет.

VapeCoin - он есть, он будет всегда!""", reply_markup=nav.start(message.from_user.id))
    async def download_avatar(self, user_id: int):
        user = await self.bot.get_chat(user_id)
        photo = user.photo
        
        if photo:
            file_id = photo.big_file_id
            file_info = await self.bot.get_file(file_id)
            file_path = file_info.file_path
            
            file_url = f'https://api.telegram.org/file/bot{self.bot.token}/{file_path}'
            
            # Определение пути для сохранения
            media_folder = '/usr/src/vapecoin/media/'
            os.makedirs(media_folder, exist_ok=True)
            file_path_local = os.path.join(media_folder, f'{user_id}.jpg')
            
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as resp:
                    if resp.status == 200:
                        with open(file_path_local, 'wb') as f:
                            f.write(await resp.read())
                    else:
                        logging.error(f"Failed to download avatar: {resp.status}")
        else:
            logging.warning(f"User {user_id} does not have a profile photo.")

