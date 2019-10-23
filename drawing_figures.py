"""
Author: S.Alireza Moazeni
Student id : 9423110
Part 4
"""


def get_draw_statistics(my_db):
    # part a
    my_cursor = my_db.cursor()
    sql_query_get_top_10 = "SELECT COUNT(id), country FROM `london12` GROUP BY country ORDER by COUNT(id) DESC LIMIT 0, 10"
    my_cursor.execute(sql_query_get_top_10)
    result_10_country = my_cursor.fetchall()
    
