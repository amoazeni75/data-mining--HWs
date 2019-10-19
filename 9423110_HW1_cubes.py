# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:21:12 2019
@author: S.Alirzea Moazeni
Data mining Homework 1
"""
import olap_cubes.prepare_database as pdata
from mysql import connector

def main():
    my_db = connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="olapdb"
    )
    pdata.insert_data_into_database(my_db)
    
    
if __name__ == '__main__':
    main()