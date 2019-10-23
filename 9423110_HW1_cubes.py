# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:21:12 2019
@author: S.Alirzea Moazeni
Data Mining Homework 1
"""
import prepare_database as pdata
import indexing as inx
import drawing_figures as part4
from mysql import connector


def main():
    my_db = connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="olapdb"
    )
    # part 2 of HW
    #pdata.insert_data_into_database(my_db)

    # part 3 of HW
    inx.create_indexes_on_table(my_db)

    # part 4 of HW
    part4.get_draw_statistics(my_db)

    
if __name__ == '__main__':
    main()