import sqlite3
from dataclasses import asdict
from typing import Union

import psycopg2
import psycopg2.extras
from dotenv import dotenv_values
from dateutil.parser import parse

from load_classes import (Film_work, Genre, Genre_film_work, Person, Person_film_work)


class SqliteMenedger:

    def __init__(self):

        self.db = sqlite3.connect("sqlite_to_postgres/db.sqlite")

        def dict_factory(cursor, row):

            d = {}

            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]

            return d

        self.db.row_factory = dict_factory
        self.offset = 0

    def get_count_rows(self, table_name: str) -> int:
        """Получает на вход имя таблицы и возваршает количетво строк в ней

        Args:
            table_name (str): Имя таблицы

        Returns:
            int: Количество строк
        """        
        self.cur = self.db.cursor()
        self.cur.execute(f"SELECT COUNT(id) FROM {table_name}")
        row_count = self.cur.fetchone()
        self.cur.close()
        return row_count['COUNT(id)']

    def fetch_data(self, table_name: str) -> Union[list[Genre], list[Film_work], list[Genre_film_work],
                                                   list[Person], list[Person_film_work]]:
        """Получает на вход имя таблицы база sqlite и возвращает лист
        обьектов датакласов Film_work, Genre, Genre_film_work, Person, Person_film_work"""

        self.cur = self.db.cursor()
        self.cur.execute(f"SELECT * FROM {table_name} LIMIT 10 OFFSET {self.offset}")
        rows_pack = self.cur.fetchmany(10)
        self.cur.close()

        if table_name == "genre":
            data_pack = [
                (
                    Genre(
                        id=row["id"],
                        name=row["name"],
                        description=row["description"],
                        created_at=parse(row["created_at"]),
                        updated_at=parse(row["updated_at"]),
                    )
                )
                for row in rows_pack
            ]
        elif table_name == "film_work":
            data_pack = [
                (
                    Film_work(
                        id=row["id"],
                        title=row["title"],
                        description=row["description"],
                        creation_date=row["creation_date"],
                        certificate=row["certificate"],
                        file_path=row["file_path"],
                        rating=row["rating"],
                        type=row["type"],
                        created_at=parse(row["created_at"]),
                        updated_at=parse(row["updated_at"]),
                    )
                )
                for row in rows_pack
            ]
        elif table_name == "genre_film_work":
            data_pack = [
                (
                    Genre_film_work(
                        id=row["id"],
                        film_work_id=row["film_work_id"],
                        genre_id=row["genre_id"],
                        created_at=parse(row["created_at"]),
                    )
                )
                for row in rows_pack
            ]
        elif table_name == "person":
            data_pack = [
                (
                    Person(
                        id=row["id"],
                        full_name=row["full_name"],
                        birth_date=row["birth_date"],
                        created_at=parse(row["created_at"]),
                        updated_at=parse(row["updated_at"]),
                    )
                )
                for row in rows_pack
            ]
        elif table_name == "person_film_work":
            data_pack = [
                (
                    Person_film_work(
                        id=row["id"],
                        film_work_id=row["film_work_id"],
                        person_id=row["person_id"],
                        role=row["role"],
                        created_at=parse(row["created_at"]),
                    )
                )
                for row in rows_pack
            ]

        self.offset += 10
        return data_pack


class PostgreMenedger:

    def __init__(self, schema) -> None:

        self.schema = schema

        self.dsn = dotenv_values("sqlite_to_postgres/.env")

        self.offset = 0

        self.sql_command = {
                "genre": f"""
                            INSERT INTO {self.schema}.genre (id, name, description, created_at, updated_at)
                            VALUES (%(id)s, %(name)s, %(description)s, %(created_at)s, %(updated_at)s)
                            ON CONFLICT (id)
                            DO UPDATE SET name=EXCLUDED.name, description=EXCLUDED.description,
                                created_at=EXCLUDED.created_at, updated_at=EXCLUDED.updated_at
                                """,

                "film_work": f"""
                            INSERT INTO {self.schema}.film_work (id, title, description, creation_date,
                                certificate, file_path, rating, type, created_at, updated_at)
                            VALUES (%(id)s, %(title)s, %(description)s, %(creation_date)s, %(certificate)s,
                                %(file_path)s, %(rating)s, %(type)s, %(created_at)s, %(updated_at)s)
                            ON CONFLICT (id)
                            DO UPDATE SET title=EXCLUDED.title, description=EXCLUDED.description,
                                creation_date=EXCLUDED.creation_date, certificate=EXCLUDED.certificate,
                                file_path=EXCLUDED.file_path, rating=EXCLUDED.rating, type=EXCLUDED.type,
                                created_at=EXCLUDED.created_at, updated_at=EXCLUDED.updated_at
                            """,

                "genre_film_work": f"""
                            INSERT INTO {self.schema}.genre_film_work (id, film_work_id, genre_id, created_at)
                            VALUES (%(id)s, %(film_work_id)s, %(genre_id)s, %(created_at)s)
                            ON CONFLICT (id)
                            DO UPDATE SET film_work_id=EXCLUDED.film_work_id, genre_id=EXCLUDED.genre_id,
                                created_at=EXCLUDED.created_at
                            """,

                "person": f"""
                            INSERT INTO {self.schema}.person (id, full_name, birth_date, created_at, updated_at)
                            VALUES (%(id)s, %(full_name)s, %(birth_date)s, %(created_at)s, %(updated_at)s)
                            ON CONFLICT (id)
                            DO UPDATE SET full_name=EXCLUDED.full_name, birth_date=EXCLUDED.birth_date,
                                created_at=EXCLUDED.created_at, updated_at=EXCLUDED.updated_at
                            """,

                "person_film_work": f"""
                            INSERT INTO {self.schema}.person_film_work (id, film_work_id,
                                person_id, role, created_at)
                            VALUES (%(id)s, %(film_work_id)s, %(person_id)s, %(role)s, %(created_at)s)
                            ON CONFLICT (id)
                            DO UPDATE SET film_work_id=EXCLUDED.film_work_id, person_id=EXCLUDED.person_id,
                                role=EXCLUDED.role, created_at=EXCLUDED.created_at
                            """}

    def insert_data(self, table_name: str, data_pack: Union[list[Genre], list[Film_work], list[Genre_film_work],
                                                            list[Person], list[Person_film_work]]) -> None:
        """Получает на вход лист обьектов датакласов Film_work, Genre, Genre_film_work,
        Person, Person_film_work и загружает их в базу данных postgres"""

        with psycopg2.connect(**self.dsn) as conn, conn.cursor() as cursor:

            for data in data_pack:
                cursor.execute(self.sql_command[table_name], asdict(data))

    def get_rows_count(self, table_name: str) -> int:
        """Получает на вход имя таблицы и возварщает количество строк в ней

        Args:
            table_name (str): Имя таблицы

        Returns:
            int: Количество строк
        """

        with psycopg2.connect(**self.dsn) as conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            rows_count = cursor.fetchone()
            return rows_count[0]

    def fetch_data(self, table_name: str) -> Union[list[Genre], list[Film_work], list[Genre_film_work],
                                                   list[Person], list[Person_film_work]]:
        """Получает на вход имя таблицы база psql и возвращает лист
        обьектов датакласов Film_work, Genre, Genre_film_work, Person, Person_film_work"""

        with psycopg2.connect(**self.dsn) as conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 10 OFFSET {self.offset}")
            rows_pack = cursor.fetchmany(10)

            if table_name == "genre":
                data_pack = [
                    (
                        Genre(
                            id=row["id"],
                            name=row["name"],
                            description=row["description"],
                            created_at=row["created_at"],
                            updated_at=row["updated_at"],
                            )
                    )
                    for row in rows_pack
                ]

            elif table_name == "film_work":
                data_pack = [
                    (
                        Film_work(
                            id=row["id"],
                            title=row["title"],
                            description=row["description"],
                            creation_date=row["creation_date"],
                            certificate=row["certificate"],
                            file_path=row["file_path"],
                            rating=row["rating"],
                            type=row["type"],
                            created_at=row["created_at"],
                            updated_at=row["updated_at"],
                        )
                    )
                    for row in rows_pack
                ]

            elif table_name == "genre_film_work":
                data_pack = [
                    (
                        Genre_film_work(
                            id=row["id"],
                            film_work_id=row["film_work_id"],
                            genre_id=row["genre_id"],
                            created_at=row["created_at"],
                        )
                    )
                    for row in rows_pack
                ]

            elif table_name == "person":
                data_pack = [
                    (
                        Person(
                            id=row["id"],
                            full_name=row["full_name"],
                            birth_date=row["birth_date"],
                            created_at=row["created_at"],
                            updated_at=row["updated_at"],
                        )
                    )
                    for row in rows_pack
                ]

            elif table_name == "person_film_work":
                data_pack = [
                    (
                        Person_film_work(
                            id=row["id"],
                            film_work_id=row["film_work_id"],
                            person_id=row["person_id"],
                            role=row["role"],
                            created_at=row["created_at"],
                        )
                    )
                    for row in rows_pack
                ]

        self.offset += 10
        return data_pack