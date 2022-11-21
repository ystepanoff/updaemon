import asyncio
import aiomysql


class DBHandler:
    def __init__(
            self,
            host: str = 'updaemon-db',
            port: int = 3306,
            user: str = 'root',
            password: str = '',
            name: str = 'updaemon',
            loop: asyncio.AbstractEventLoop = None
    ) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.name = name
        self.loop = loop
        self.pool = None


    async def setup(self) -> None:
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.name,
            loop=self.loop,
        )


    async def destroy(self) -> None:
        self.pool.close()
        await self.pool.wait_closed()


    async def test_mysql(self) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 42;")
                print(cur.description)
                (r,) = await cur.fetchone()
                print(r)