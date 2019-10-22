# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 19:46:33 2019
@author: S.Alireza Moazeni
Data Mining Homework 1
Part 2
"""
from __future__ import print_function
import pandas as pd


def insert_data_into_database(my_db):
    print("Part 2: Inserting data to the database")
    # 1. Prepare SQL data in memory
    london12 = pd.read_csv('london12.csv')
    country_continent = pd.read_csv('countries_by_continent.csv')
    my_cursor = my_db.cursor()
    my_cursor.execute("DELETE FROM `london12` WHERE 1")
    my_cursor.execute("ALTER TABLE  `london12` AUTO_INCREMENT = 1")
    my_db.commit()
    for index, row in london12.iterrows():
        # if row["Country"] == "United States of America":
        #     x = 0
        continent = get_continent(row["Country"], country_continent)
        # print(str(index) + " country : " + row["Country"] + " , continent : " + continent)
        age_group = get_age_group(row["Age"])
        sql = "INSERT INTO `london12` (`id`, `continent`, `country`, `gender`, `agegroup`, `sport`, `gold`, `silver`, `bronze`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (index + 1, continent, row["Country"], row["Gender"], age_group,
               row["Sport"], row["Gold Medals"], row["Silver Medals"], row["Bronze Medals"])
        my_cursor.execute(sql, val)
        if index % 1000 == 0 and index != 0:
            print(str(index) + " data added")
    
    my_db.commit()
    print("All data successfully added to the database")
    print("#################################################")


def get_continent(country_input, continents):
    for index, continent_country in continents.iterrows():
        # if continent_country["Country"] == "United Arab Emirates":
        #     x = 0
        if check_equality_countries(country_input, continent_country["Country"]):
            return continent_country["Continent"]
    return -1


def check_equality_countries(country_input, country_csv):
    # 1: convert to lowercase
    country_input = country_input.lower()
    country_csv = country_csv.lower()
    # 2: simple match
    if country_input == country_csv:
        return True
    # 3: remove stop words
    country_csv = country_csv.split(" ")
    country_input = country_input.split(" ")
    country_csv = remove_stop_words(country_csv)
    country_input = remove_stop_words(country_input)
    # 4: check equality foreach item
    common_items = list(set(country_input).intersection(country_csv))
    if len(common_items) != 0:
        for word in common_items:
            if word != "states" and word != "united":
                return True
    # 5: check abbreviation
    # abb1 = get_abbreviation(country_input)
    # abb2 = get_abbreviation(country_csv)
    # if abb1 == country_csv or abb2 == country_input or abb2 == abb1:
    #     return True
    return False


def remove_stop_words(name):
    # we remove any word of this collection from the name of countries
    remove_words = ["people's", "republic", "of", "democratic", "and"]
    for word in name:
        if word in remove_words:
            name.remove(word)
    for index, word in enumerate(name):
        if "(" in word and ")" in word:
            word = word.replace("(", "")
            word = word.replace(")", "")
            name[index] = word
    return name


def get_abbreviation(words):
    abb = ""
    for word in words:
        if len(word) != 0:
            abb += word[0]
    return abb


def get_age_group(age):
    if age < 20:
        return "A"
    elif 20 <= age < 25:
        return "B"
    elif 25 <= age < 30:
        return "C"
    else:
        return "D"

