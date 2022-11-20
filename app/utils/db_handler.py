import aiomysql


class DBHandler:
    def __init__(self, host='updaemon-db', port=3306, user='root', password='', name='updaemon', loop=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.name = name
        self.loop = loop
        self.pool = None


    async def setup(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.name,
            loop=self.loop,
        )


    async def destroy(self):
        self.pool.close()
        await self.pool.wait_closed()


    async def test_mysql(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 42;")
                print(cur.description)
                (r,) = await cur.fetchone()
                print(r)