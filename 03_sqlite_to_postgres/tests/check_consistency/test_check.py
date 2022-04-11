from load_classes import PostgreMenedger, SqliteMenedger

sqlite = SqliteMenedger()
postgre = PostgreMenedger('content')


def test_check_consistency():
    for table_name in postgre.sql_command.keys():
        while True:
            sqlite_data = sqlite.fetch_data(table_name)
            psql_data = postgre.fetch_data(table_name)
            assert sqlite_data == psql_data

            if not sqlite_data:
                break

        sqlite.offset = 0


def test_check_rows_count():
    for table_name in postgre.sql_command.keys():
        sqlite_row_count = sqlite.get_count_rows(table_name)
        psql_row_count = postgre.get_rows_count(table_name)
        assert sqlite_row_count == psql_row_count
