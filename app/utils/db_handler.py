import asyncio
import aiomysql
import pymysql
import json
import logging
from typing import List, Tuple, Dict, Any, Optional


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
                    autocommit=True,
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

    async def list_sources(self) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT id, name, description, params FROM source")
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
                    INSERT INTO source
                        (name, description, params)
                    VALUES
                        (%(name)s, %(description)s, %(params)s)
                """, {
                    'name': name,
                    'description': description,
                    'params': json.dumps(params, ensure_ascii=False),
                })

    async def latest_state(self, source_id: int) -> Optional[str]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT data, updated_at FROM state WHERE source_id = %s", (source_id,))
                if cur.rowcount > 0:
                    return cur.fetchone()
        return None

    async def upsert_state(self, source_id: int, state: str) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO state
                        (source_id, data, updated_at)
                    VALUES
                        (%(source_id)s, %(state)s, NOW())
                    ON DUPLICATE KEY UPDATE
                        data = %(state)s,
                        updated_at = NOW()
                """, {
                    'source_id': source_id,
                    'state': state,
                })
