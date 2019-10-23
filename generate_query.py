"""
Author: S.Alireza Moazeni
Student_ID: 9423110
Part 6: generate all proper query
"""
import itertools

query_template = []
all_result_query = []

gender = ["F", "M"]
agegroup = ["A", "B", "C", "D"]
continent = ["Africa", "Asia", "Europe", "North America", "Oceania", "Other", "South America"]
sport = ["Archery", "Athletics", "Badminton", "Basketball", "Beach Volleyball", "Canoe Slalom",
         "Canoe Sprint", "Cycling - BMX", "Cycling - Mountain Bike", "Cycling - Road", "Cycling - Track",
         "Diving", "Equestrian", "Fencing", "Football", "Handball", "Hockey", "Judo", "Modern Pentathlon",
         "Rowing", "Sailing", "Shooting", "Swimming", "Table Tennis", "Tennis", "Triathlon", "Volleyball",
         "Water Polo", "Weightlifting", "Wrestling"]


def generate_query(my_db):
    x = get_terms(2, [])
    print("Part 6: Generate all queries")
    for i in range(5):
        number_terms_in_where = i
        upper_bound_group_by = 5 - i
        # here we have all combination that size of each of them is number_terms_in_where
        where_terms = get_terms(number_terms_in_where, [])
        for where_set in list(where_terms):
            where_set = list(where_set)
            for j in range(upper_bound_group_by):
                group_by_terms = get_terms(j, where_set)
                for group_set in list(group_by_terms):
                    group_set = list(group_set)
                    res = get_query(where_set, group_set)
                    print(res)
                    query_template.append([where_set, group_set])

    print("Actual queries : ")
    # each item in query_template includes two list that the first one is the variables in where clause
    # and the second one is the variables in group by clause
    for query_temp in query_template:
        # if the size of query[0] = where clause == 0, so we will not have any value
        query_values = get_all_condition(query_temp[0])
        #print("-----------------")
        #print(query_values)
        #print(query_temp)
        get_final_query_with_value(query_temp, query_values)
        #print("-----------------")

    print("**************")
    for i in all_result_query:
        print(i)


def get_terms(count, forbidden_list):
    all_words = ["sport", "agegroup", "gender", "continent"]
    proper_list = [x for x in all_words if x not in forbidden_list]
    return itertools.combinations(proper_list, count)


def get_query(where_terms, group_by_terms):
    sql = "SELECT * FROM `london12` WHERE "
    for index, item in enumerate(where_terms):
        if index != len(where_terms) - 1:
            sql += item
            sql += " and "
        else:
            sql += item
    if len(list(where_terms)) == 0:
        sql += "1"

    if len(list(group_by_terms)) == 0:
        return sql
    sql += " GROUP BY "
    for index2, item2 in enumerate(group_by_terms):
        if index2 != len(group_by_terms) - 1:
            sql += item2
            sql += " and "
        else:
            sql += item2

    return sql


def get_all_condition(where_group_list):
    pre_list = []
    for item in where_group_list:
        if item == "gender":
            pre_list.append(gender)
        elif item == "sport":
            pre_list.append(sport)
        elif item == "continent":
            pre_list.append(continent)
        elif item == "agegroup":
            pre_list.append(agegroup)
    return list(itertools.product(*pre_list))


def get_final_query_with_value(clauses, values):
    sql = "SELECT * FROM `london12` WHERE "
    if len(values[0]) == 0:
        sql += "1 "
        if len(clauses[1]) != 0:
            sql += " GROUP BY "
            for index2, g_item in enumerate(clauses[1]):
                if index2 == len(clauses[1]) - 1:
                    sql += g_item
                else:
                    sql += g_item
                    sql += ", "
        all_result_query.append(sql)
        #print(sql)
        return
    else:
        sql = ""
        for index, value_items in enumerate(values):
            sql = "SELECT * FROM `london12` WHERE "
            for index3, m, n in zip(range(len(value_items)), clauses[0], value_items):
                sql += m
                sql += " = `"
                sql += n
                if index3 != len(value_items) - 1:
                    sql += "` and "
                else:
                    sql += "`"

            if len(clauses[1]) != 0:
                sql += " GROUP BY "
                for index2, g_item in enumerate(clauses[1]):
                    if index2 == len(clauses[1]) - 1:
                        sql += g_item
                    else:
                        sql += g_item
                        sql += ", "
            all_result_query.append(sql)
            #print(sql)

