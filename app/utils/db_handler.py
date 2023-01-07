from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging
import json
import asyncio
import aiomysql
import pymysql


@dataclass
class DBParams:
    host: str = 'updaemon-db'
    port: str = 3306
    user: str = 'root'
    password: str = ''
    name: str = 'updaemon'


class DBHandler:
    def __init__(
            self,
            params: DBParams,
    ) -> None:
        self.params = params
        self.loop = asyncio.get_event_loop()
        self.logger = logging.getLogger(__name__)
        self.pool = None

    async def setup(self) -> None:
        async def create_pool():
            try:
                self.pool = await aiomysql.create_pool(
                    host=self.params.host,
                    port=self.params.port,
                    user=self.params.user,
                    password=self.params.password,
                    db=self.params.name,
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
                await cur.execute("SELECT id, name, description, type, remote FROM source")
                return [
                    {
                        'id': source_id,
                        'name': name,
                        'description': description,
                        'type': type_,
                        'remote': remote,
                    } for (source_id, name, description, type_, remote) in await cur.fetchall()
                ]

    async def add_source(self, name: str, description: str, type_: str, remote: str) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO source
                        (name, description, type_, remote)
                    VALUES
                        (%(name)s, %(description)s, %(type)s, %(remote)s)
                """, {
                    'name': name,
                    'description': description,
                    'type': type_,
                    'remote': remote,
                })

    async def latest_state(self, source_id: int) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT data, updated_at FROM state WHERE source_id = %s
                """, (source_id,))
                if cur.rowcount > 0:
                    data, updated_at = await cur.fetchone()
                    return {
                        'data': data,
                        'updated_at': updated_at,
                    }
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

    async def find_scraper(self, source_id: int) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT scraper.base_class, source_scraper.params
                    FROM scraper
                    INNER JOIN source_scraper ON scraper.id = source_scraper.scraper_id
                    WHERE source_scraper.source_id = %(source_id)s
                """, {
                    'source_id': source_id,
                })
                if cur.rowcount > 0:
                    base_class, params = await cur.fetchone()
                    return {
                        'base_class': base_class,
                        'params': json.loads(params),
                    }
        return None

    async def list_actions(self, source_id: int) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT action.base_class, COALESCE(action.params_config, '{}'), source_action.params
                    FROM action
                    INNER JOIN source_action ON action.id = source_action.action_id
                    WHERE source_action.source_id = %(source_id)s
                """, {
                    'source_id': source_id,
                })
                return [
                    {
                        'base_class': base_class,
                        'params_config': json.loads(params_config),
                        'params': json.loads(params),
                    } for base_class, params_config, params in await cur.fetchall()
                ]
