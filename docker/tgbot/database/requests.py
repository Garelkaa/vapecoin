import logging
from sqlalchemy.future import select
from .models import User, Refferer, AsyncSessionLocal

logging.basicConfig(level=logging.INFO)

class DBUsers:
    def __init__(self):
        self.session = AsyncSessionLocal()

    async def add_user(self, user_id: int, username_tg: str, password: str):
        async with self.session.begin():
            try:
                new_user = User(user_id_tg=user_id, energy=100, money=0, moneyhour=0, image=f'media/{user_id}.jpg', username_tg=username_tg, password=password)
                self.session.add(new_user)
                await self.session.commit()
            except Exception as e:
                logging.error(f"Failed to add user: {e}")
                await self.session.rollback()


    async def find_user(self, user_id: int):
        async with self.session.begin():
            try:
                result = await self.session.execute(select(User).filter(User.user_id_tg == user_id))
                user = result.scalars().first()
                if user:
                    return user.id
                return None
            except Exception as e:
                logging.error(f"Failed to find user: {e}")
                return None
    

    async def increase_user_money(self, user_id: int, amount: int):
        async with self.session.begin():
            try:
                if amount >= 0:
                    result = await self.session.execute(select(User).filter(User.id == user_id))
                    user = result.scalars().first()
                    if user:
                        user.money += amount
                        await self.session.commit()
                        return True
                return False
            except Exception as e:
                logging.error(f"Failed to increase user's money: {e}")
                await self.session.rollback()
                return False

class DBReferrals:
    def __init__(self):
        self.session = AsyncSessionLocal()

    async def add_user(self, user_id_id: int, ref_link: str, ref_user_id: int):
        try:
            new_referrer = Refferer(user_id_id=user_id_id, ref_link=ref_link, ref_user_id_id=ref_user_id)
            self.session.add(new_referrer)
            await self.session.commit()  # Await the commit coroutine
        except Exception as e:
            logging.error(f"Failed to add referrer: {e}")
            await self.session.rollback()
        finally:
            await self.session.close()  # Await the close coroutine

