from __future__ import annotations
from typing import Optional, List, Dict, Any
from flask_login import UserMixin
import json

from . import db


class User(UserMixin):
    def __init__(self, email: str, password: str = None, name: str = None) -> None:
        self.user_id = None
        self.email = email
        self.password = password
        self.name = name

    @classmethod
    def from_id(cls, user_id: int) -> Optional[User]:
        with db.get_db().cursor() as cur:
            cur.execute("SELECT email, password, name FROM user WHERE id = %s", user_id)
            if cur.rowcount > 0:
                return User(*cur.fetchone())
        return None

    def get_id(self) -> Optional[int]:
        with db.get_db().cursor() as cur:
            cur.execute("SELECT id FROM user WHERE email = %s", self.email)
            (self.user_id,) = cur.fetchone()
        return self.user_id

    def exists(self) -> bool:
        result = False
        with db.get_db().cursor() as cur:
            cur.execute("SELECT id, password, name FROM user WHERE email = %s", self.email)
            if cur.rowcount > 0:
                self.user_id, self.password, self.name = cur.fetchone()
                result = True
        return result

    def persist(self) -> None:
        with db.get_db().cursor() as cur:
            cur.execute("""
                INSERT INTO user
                    (email, password, name)
                VALUES
                    (%(email)s, %(password)s, %(name)s)
            """, {
                'email': self.email,
                'password': self.password,
                'name': self.name,
            })

    def list_sources(self):
        with db.get_db().cursor() as cur:
            cur.execute("SELECT id, name, description, remote FROM source WHERE user_id = %s", self.get_id())
            return [
                {
                    'id': source_id,
                    'name': name,
                    'description': description,
                    'remote': remote,
                } for source_id, name, description, remote in cur.fetchall()
            ]


class Source:
    def __init__(
            self,
            user_id: int,
            name: str = None,
            description: str = None,
            remote: str = None,
            scraper_id: int = None,
            params: str = None,
    ) -> None:
        self.user_id = user_id
        self.name = name
        self.description = description
        self.remote = remote
        self.scraper_id = scraper_id
        self.params = params

    @classmethod
    def from_id(cls, source_id: int, user_id: int) -> Optional[Source]:
        with db.get_db().cursor() as cur:
            cur.execute("""
                SELECT
                    user_id, name, description, remote, scraper_id, COALESCE(params, '{}')
                FROM source
                WHERE id = %(id)s AND user_id = %(user_id)s
            """, {
                'id': source_id,
                'user_id': user_id,
            })
            if cur.rowcount > 0:
                return Source(*cur.fetchone())
        return None

    @classmethod
    def list_actions(cls, source_id: int, user_id: int) -> List[Dict[str, Any]]:
        with db.get_db().cursor() as cur:
            cur.execute("""
                SELECT
                    action.id, action.base_class, COALESCE(action.params_config, '{}'), source_action.id, source_action.params
                FROM action
                INNER JOIN source_action
                ON action.id = source_action.action_id
                WHERE source_id = %(source_id)s
                AND source_id in (SELECT id FROM source WHERE user_id = %(user_id)s)
            """, {
                'source_id': source_id,
                'user_id': user_id,
            })
            return [
                {
                    'id': action_id,
                    'base_class': base_class,
                    'source_action_id': source_action_id,
                    'params_config': params_config,
                    'params': params,
                } for action_id, base_class, params_config, source_action_id, params in cur.fetchall()
            ]

    def update(self, source_id: int) -> None:
        with db.get_db().cursor() as cur:
            cur.execute("""
                UPDATE source
                SET
                    user_id = %(user_id)s,
                    name = %(name)s,
                    description = %(description)s,
                    remote = %(remote)s,
                    scraper_id = %(scraper_id)s,
                    params = %(params)s
                WHERE id = %(source_id)s
            """, {
                'source_id': source_id,
                'user_id': self.user_id,
                'name': self.name,
                'description': self.description,
                'remote': self.remote,
                'scraper_id': self.scraper_id,
                'params': json.dumps(self.params),
            })

    def delete(self, source_id: int) -> None:
        with db.get_db().cursor() as cur:
            cur.execute("DELETE FROM source_action WHERE source_id = %s", source_id)
            cur.execute("DELETE FROM state WHERE source_id = %s", source_id)
            cur.execute("DELETE FROM source WHERE id = %s", source_id)

    def save(self):
        with db.get_db().cursor() as cur:
            cur.execute("""
                INSERT INTO source
                    (user_id, name, description, remote, scraper_id, params)
                VALUES
                    (%(user_id)s, %(name)s, %(description)s, %(remote)s, %(scraper_id)s, %(params)s)
            """, {
                'user_id': self.user_id,
                'name': self.name,
                'description': self.description,
                'remote': self.remote,
                'scraper_id': self.scraper_id,
                'params': json.dumps(self.params),
            })
            db.get_db().commit()


class Action:
    def __init__(self, base_class: str) -> None:
        self.base_class = base_class

    @classmethod
    def list_base_actions(cls):
        with db.get_db().cursor() as cur:
            cur.execute("SELECT id, base_class FROM action")
            return [
                {
                    'id': action_id,
                    'base_class': base_class,
                } for action_id, base_class in cur.fetchall()
            ]


class SourceAction:
    def __init__(self, source_id: int, action_id: int, params: Dict[str, Any]) -> None:
        self.source_id = int(source_id)
        self.action_id = int(action_id)
        self.params = params

    @classmethod
    def from_id(cls, source_action_id: int, user_id: int) -> Optional[SourceAction]:
        with db.get_db().cursor() as cur:
            cur.execute("""
                SELECT
                    source_id, action_id, COALESCE(params, '{}')
                FROM source_action
                WHERE id = %(id)s
                AND source_id in (SELECT id FROM source WHERE user_id = %(user_id)s)
            """, {
                'id': source_action_id,
                'user_id': user_id,
            })
            if cur.rowcount > 0:
                return SourceAction(*cur.fetchone())
        return None

    def update(self, source_action_id: int) -> None:
        with db.get_db().cursor() as cur:
            cur.execute("""
                UPDATE source_action
                SET
                    source_id = %(source_id)s,
                    action_id = %(action_id)s,
                    params = %(params)s
                WHERE
                    id = %(id)s
            """, {
                'id': source_action_id,
                'source_id': self.source_id,
                'action_id': self.action_id,
                'params': json.dumps(self.params),
            })

    def save(self) -> None:
        with db.get_db().cursor() as cur:
            cur.execute("""
                INSERT INTO source_action (source_id, action_id, params)
                VALUES (%(source_id)s, %(action_id)s, %(params)s)
            """, {
                'source_id': self.source_id,
                'action_id': self.action_id,
                'params': json.dumps(self.params),
            })

    def delete(self, source_action_id: int) -> None:
        with db.get_db().cursor() as cur:
            cur.execute("DELETE FROM source_action WHERE id = %s", source_action_id)


class Scraper:
    def __init__(self, base_class: str, params_config: str = None):
        self.base_class = base_class
        self.params_config = params_config

    @classmethod
    def list_base_scrapers(cls):
        with db.get_db().cursor() as cur:
            cur.execute("SELECT id, base_class, params_config FROM scraper")
            return [
                {
                    'id': scraper_id,
                    'base_class': base_class,
                    'params_config': params_config,
                } for scraper_id, base_class, params_config in cur.fetchall()
            ]