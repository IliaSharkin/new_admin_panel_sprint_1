from dataclasses import asdict
from typing import Union

import psycopg2
import psycopg2.extras
from dotenv import dotenv_values

from data_classes import (Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork)


class PostgreMenedger:

    def __init__(self, schema) -> None:

        self.schema = schema

        self.dsn = dotenv_values("03_sqlite_to_postgres/.env")

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
                                file_path, rating, type, created_at, updated_at)
                            VALUES (%(id)s, %(title)s, %(description)s, %(creation_date)s,
                            %(file_path)s, %(rating)s, %(type)s, %(created_at)s, %(updated_at)s)
                            ON CONFLICT (id)
                            DO UPDATE SET title=EXCLUDED.title, description=EXCLUDED.description,
                                creation_date=EXCLUDED.creation_date, file_path=EXCLUDED.file_path,
                                rating=EXCLUDED.rating, type=EXCLUDED.type, created_at=EXCLUDED.created_at,
                                updated_at=EXCLUDED.updated_at
                            """,

                "genre_film_work": f"""
                            INSERT INTO {self.schema}.genre_film_work (id, film_work_id, genre_id, created_at)
                            VALUES (%(id)s, %(film_work_id)s, %(genre_id)s, %(created_at)s)
                            ON CONFLICT (id)
                            DO UPDATE SET film_work_id=EXCLUDED.film_work_id, genre_id=EXCLUDED.genre_id,
                                created_at=EXCLUDED.created_at
                            """,

                "person": f"""
                            INSERT INTO {self.schema}.person (id, full_name, created_at, updated_at)
                            VALUES (%(id)s, %(full_name)s,%(created_at)s, %(updated_at)s)
                            ON CONFLICT (id)
                            DO UPDATE SET full_name=EXCLUDED.full_name,
                                created_at=EXCLUDED.created_at, updated_at=EXCLUDED.updated_at
                            """,

                "person_film_work": f"""
                            INSERT INTO {self.schema}.person_film_work (id, film_work_id,
                                person_id, role, created_at)
                            VALUES (%(id)s, %(film_work_id)s, %(person_id)s, %(role)s, %(created_at)s)
                            ON CONFLICT (film_work_id, person_id)
                            DO UPDATE SET film_work_id=EXCLUDED.film_work_id, person_id=EXCLUDED.person_id,
                                role=EXCLUDED.role, created_at=EXCLUDED.created_at 
                            """}

    def insert_data(self, table_name: str, data_pack: Union[list[Genre], list[Filmwork], list[GenreFilmwork],
                                                            list[Person], list[PersonFilmwork]]) -> None:
        """Получает на вход лист обьектов датакласов Filmwork, Genre, Genre_film_work,
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

    def fetch_data(self, table_name: str) -> Union[list[Genre], list[Filmwork], list[GenreFilmwork],
                                                   list[Person], list[PersonFilmwork]]:
        """Получает на вход имя таблицы база psql и возвращает лист
        обьектов датакласов Film_work, Genre, Genre_film_work, Person, Person_film_work"""
        with psycopg2.connect(**self.dsn) as conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 10 OFFSET {self.offset}")
            rows_pack = cursor.fetchmany(10)

            match table_name:
                case 'genre':
                    data_pack = [
                        (Genre(**row)) for row in rows_pack
                        ]

                case "film_work":
                    data_pack = [
                        (Filmwork(**row)) for row in rows_pack
                    ]

                case "genre_film_work":
                    data_pack = [
                        (GenreFilmwork(**row)) for row in rows_pack
                    ]

                case "person":
                    data_pack = [
                        (Person(**row)) for row in rows_pack
                    ]

                case "person_film_work":
                    data_pack = [
                        (PersonFilmwork(**row)) for row in rows_pack
                    ]

        self.offset += 10
        return data_pack
