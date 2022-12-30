from flask_login import UserMixin
from typing import Optional
from web import db


class User(UserMixin):
    def __init__(self, email: str, password: str = None, name: str = None) -> None:
        self.id = None
        self.email = email
        self.password = password
        self.name = name

    def get_id(self) -> Optional[int]:
        with db.get_db().cursor() as cur:
            cur.execute("SELECT id FROM user WHERE email = %s", self.email)
            (self.id,) = cur.fetchone()
        return self.id

    def exists(self) -> bool:
        result = False
        with db.get_db().cursor() as cur:
            cur.execute("SELECT id, password, name FROM user WHERE email = %s", self.email)
            if cur.rowcount > 0:
                self.id, self.password, self.name = cur.fetchone()
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
                    'id': id,
                    'name': name,
                    'description': description,
                    'remote': remote,
                } for id, name, description, remote in cur.fetchall()
            ]


def find_user_by_id(user_id: int) -> Optional[User]:
    with db.get_db().cursor() as cur:
        cur.execute("SELECT email, password, name FROM user WHERE id = %s", user_id)
        if cur.rowcount > 0:
            return User(*cur.fetchone())
    return None
