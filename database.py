import asyncio
import asyncpg


class Database:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                user='povad1r',
                database='neondb',
                password='mUlN0H2hIspZ',
                host='ep-old-heart-356850.eu-central-1.aws.neon.tech',
                port='5432'
            )
        )

    async def register_user(self, first_name, username, telegram_id):
        sql = f"""
        INSERT INTO footballbot_users (first_name, username, telegram_id)
        VALUES ('{first_name}', '{username}', '{telegram_id}')
        """
        await self.pool.execute(sql)

    async def check_user(self, telegram_id):
        sql = f"""
        SELECT * FROM footballbot_users WHERE telegram_id = '{telegram_id}'
        """
        result = await self.pool.fetchrow(sql)
        return result

    async def add_favourite_player(self, favourite_player, telegram_id):
        sql = f"""
        UPDATE footballbot_users
        SET favourite_player = '{favourite_player}'
        WHERE telegram_id = '{telegram_id}'
        """
        await self.pool.execute(sql)

    async def change_favourite_player(self, new_favourite_player, telegram_id):
        sql = f"""
        UPDATE footballbot_users
        SET favourite_player = '{new_favourite_player}'
        WHERE telegram_id = '{telegram_id}'
        """
        await self.pool.execute(sql)

    async def check_favourite_player(self, telegram_id):
        sql = f"""
        SELECT favourite_player FROM footballbot_users WHERE telegram_id = '{telegram_id}'
        """
        result = await self.pool.fetchrow(sql)
        return print(result)