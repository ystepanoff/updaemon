import asyncio
import aiomysql
import pymysql
import json
import logging
from typing import List, Tuple, Dict, Any


class DBHandler:
    def __init__(
            self,
            host: str = 'updaemon-db',
            port: int = 3306,
            user: str = 'root',
            password: str = '',
            name: str = 'updaemon',
            loop: asyncio.AbstractEventLoop = None,
    ) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.name = name
        self.loop = loop
        self.pool = None
        self.logger = logging.getLogger(__name__)

    async def setup(self) -> None:
        async def create_pool():
            try:
                self.pool = await aiomysql.create_pool(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    db=self.name,
                    loop=self.loop,
                )
                return True
            except pymysql.err.OperationalError:
                self.logger.error("Cannot connect to the DB!")
                return False

        while True:
            try_pool = await create_pool()
            if try_pool is True:
                break
            await asyncio.sleep(10)

    async def destroy(self) -> None:
        self.pool.close()
        await self.pool.wait_closed()

    async def list_sources(self) -> List[Tuple[int, str, str, Dict[str, Any]]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM source")
                sources = [
                    {
                        'id': source_id,
                        'name': name,
                        'description': description,
                        'params': json.loads(params),
                    } for (source_id, name, description, params) in await cur.fetchall()
                ]
                return sources

    async def add_source(self, name: str, description: str, params: Dict[str, Any]) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO sources (name, description, params)
                    VALUES (%(name)s, %(description)s, %(params)s)
                """, {
                    'name': name,
                    'description': description,
                    'params': json.dumps(params),
                })

    async def test_mysql(self) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 42")
                print(cur.description)
                (r,) = await cur.fetchone()
                print(r)