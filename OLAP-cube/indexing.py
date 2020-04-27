"""
Author: S.Alirzea Moazeni
Student_ID: 9423110
Part 3: indexing

some useful commands
1- DROP INDEX index_name ON table_name;
2- CREATE INDEX index_name ON `table_name`(column_name_1, column_name_2) USING BTREE;
3- SHOW INDEX FROM table_name;
"""
from itertools import combinations


def create_indexes_on_table(my_db):
    print("Part 3: Indexing")
    my_cursor = my_db.cursor()
    # 1: create all combination of (continent, country, gender, agegroup, sport)
    terms_list = ["continent", "country", "gender", "agegroup", "sport"]
    for i in range(0, terms_list.__len__()):
        comb = combinations(terms_list, i + 1)
        for words_set in list(comb):
            print_log(words_set)
            sql_command_add, sql_command_remove = create_sql_index_command(words_set)
            try:
                my_cursor.execute(sql_command_remove)
                print("The index removed from the table")
            except:
                print("The index did not exist in the table")
            my_cursor.execute(sql_command_add)
    my_db.commit()
    print("#################################################")


def create_sql_index_command(words):
    sql_1 = "CREATE INDEX "
    sql_2 = " ON `london12`("
    sql_name = ""
    for index, item in enumerate(words):
        if index == len(words) - 1:
            sql_2 += item
            sql_name += item
        else:
            sql_2 += item
            sql_2 += ","
            sql_name += item
            sql_name += "_"

    sql_2 += ") USING BTREE;"
    sql_add = sql_1 + sql_name + sql_2
    sql_remove = "DROP INDEX " + sql_name + " ON `london12`;"
    return sql_add, sql_remove


def print_log(word_set):
    print_state = "indexing for "
    for item in word_set:
        print_state += item
        print_state += ", "
    print(print_state)
