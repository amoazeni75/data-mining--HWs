# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:21:12 2019

@author: S.Alirzea Moazeni

Datamining Homework 1
"""

from __future__ import print_function
from mysql import connector
import pandas as pd

print("inserting the data into the database...")

# 1. Prepare SQL data in memory

mydb = connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="olapdb"
)

london12 = pd.read_csv('london12.csv')
country_continent = pd.read_csv('countries_by_continent.csv')

# we remove any word of this collection from the name of countries
removeWords = ["people's", "republic", "of", "democratic", "and"]


mycursor = mydb.cursor()
for index, row in london12.iterrows():
#    sql = "INSERT INTO london12 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#    val = (row["continent"], row["country"], row["gender"], row["agegroup"],
#           row["sport"], row["gold"], row["silver"], row["bronze"])
#    mycursor.execute(sql, val)
    country = row["Country"]
    
    print(country)   

mydb.commit()