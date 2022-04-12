from sqlite_manager import SqliteMenedger
from psql_manager import PostgreMenedger


if __name__ == '__main__':

    sqlite = SqliteMenedger()
    postgre = PostgreMenedger('content')

    for table_name in postgre.sql_command.keys():

        while True:
            rows_pack = sqlite.fetch_data(table_name)

            if not rows_pack:
                break

            postgre.insert_data(table_name, rows_pack)

        sqlite.offset = 0
