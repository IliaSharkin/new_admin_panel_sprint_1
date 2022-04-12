import sqlite3
from data_classes import (Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork)
from typing import Union



class SqliteMenedger:

    def __init__(self):

        self.db = sqlite3.connect("03_sqlite_to_postgres/db.sqlite")

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

    def fetch_data(self, table_name: str) -> Union[list[Genre], list[Filmwork], list[GenreFilmwork],
                                                   list[Person], list[PersonFilmwork]]:
        """Получает на вход имя таблицы база sqlite и возвращает лист
        обьектов датакласов Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork"""

        self.cur = self.db.cursor()
        self.cur.execute(f"SELECT * FROM {table_name} LIMIT 10 OFFSET {self.offset}")
        rows_pack = self.cur.fetchmany(10)
        self.cur.close()

        match table_name:
            case "genre":
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
