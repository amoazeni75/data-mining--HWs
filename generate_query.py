"""
Author: S.Alireza Moazeni
Student_ID: 9423110
Part 6: generate all proper query
"""
import itertools
import math
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
query_template = []
all_result_query = []
database_connection = ""
gender = ["F", "M"]
agegroup = ["A", "B", "C", "D"]
continent = ["Africa", "Asia", "Europe", "North America", "Oceania", "Other", "South America"]
sport = ["Archery", "Athletics", "Badminton", "Basketball", "Beach Volleyball", "Canoe Slalom",
         "Canoe Sprint", "Cycling - BMX", "Cycling - Mountain Bike", "Cycling - Road", "Cycling - Track",
         "Diving", "Equestrian", "Fencing", "Football", "Handball", "Hockey", "Judo", "Modern Pentathlon",
         "Rowing", "Sailing", "Shooting", "Swimming", "Table Tennis", "Tennis", "Triathlon", "Volleyball",
         "Water Polo", "Weightlifting", "Wrestling"]


def generate_queries_template():
    print("Part 6: Generate all Queries Template")
    for i in range(5):
        number_terms_in_where = i
        upper_bound_group_by = 5 - i
        # here we have all combination that size of each of them is number_terms_in_where
        where_terms = get_all_condition_space(number_terms_in_where, [])
        for where_set in list(where_terms):
            where_set = list(where_set)
            for j in range(upper_bound_group_by):
                group_by_terms = get_all_condition_space(j, where_set)
                for group_set in list(group_by_terms):
                    group_set = list(group_set)
                    res = construct_query_template(where_set, group_set)
                    print(res)
                    query_template.append([where_set, group_set])

    # each item in query_template includes two list that the first one is the variables in where clause
    # and the second one is the variables in group by clause
    for query_temp in query_template:
        # if the size of query[0] = where clause == 0, so we will not have any value
        query_values = get_all_condition_values(query_temp[0])
        get_final_query_with_value(query_temp, query_values)

    print(bcolors.HEADER + "All Queries with Values : ")
    xx = len(all_result_query)
    for i in all_result_query:
        print(bcolors.OKGREEN + i)


def get_all_condition_space(count, forbidden_list):
    all_words = ["sport", "agegroup", "gender", "continent"]
    proper_list = [x for x in all_words if x not in forbidden_list]
    return itertools.combinations(proper_list, count)


def construct_query_template(where_terms, group_by_terms):
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


def get_all_condition_values(where_group_list):
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
    sql = construct_select_part(clauses[1])
    # add where clause
    if len(values[0]) == 0:
        sql += "1 "
        if len(clauses[1]) != 0:
            sql += " GROUP BY "
            sql = adding_group_by_to_query(sql, clauses[1])
        all_result_query.append(sql)
        return
    else:
        for index, value_items in enumerate(values):
            sql = construct_select_part(clauses[1])
            for index3, m, n in zip(range(len(value_items)), clauses[0], value_items):
                sql += m
                sql += " = \'"
                sql += n
                if index3 != len(value_items) - 1:
                    sql += "\' and "
                else:
                    sql += "\'"

            if len(clauses[1]) != 0:
                sql += " GROUP BY "
                sql = adding_group_by_to_query(sql, clauses[1])

            all_result_query.append(sql)


def adding_group_by_to_query(query, group):
    for index, g_item in enumerate(group):
        if index == len(group) - 1:
            query += g_item
            query += " "
        else:
            query += g_item
            query += ", "
    return query


def adding_where_to_query(query, where_clause, where_values, query_set):
    for index, value_items in enumerate(where_values):
        for index2, m, n in zip(range(len(value_items)), where_clause, value_items):
            query += m
            query += " = `"
            query += n
            if index2 != len(value_items) - 1:
                query += "` and "
            else:
                query += "`"
    return query


def construct_select_part(group_set):
    sql = "SELECT "
    # if we have group by, we should add them to select part
    if len(group_set) != 0:
        sql = adding_group_by_to_query(sql, group_set)
        sql += ", SUM(gold) , SUM(silver) , SUM(bronze), (SUM(gold) + SUM(silver) + SUM(bronze))"
    else:
        sql += " * "
    sql += " FROM `london12` WHERE "
    return sql


def get_query_with_most_medals_deviation(my_db):
    print("Calculation Part A of Question 6 ...")
    my_cursor = my_db.cursor()
    all_accepted_query = []
    all_accepted_deviation = []
    for query in all_result_query:
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        if len(result) < 100:
            continue
        # do not have group by
        relational_deviation = 0
        if "GROUP" not in query:
            sum_medals, all_medal_per_record = get_sum_all_medals_in_query_without_group_by(result)
            if sum_medals < 20:
                continue
            relational_deviation = calculate_deviation_without_group_by(sum_medals, all_medal_per_record)
        # we do not have anything here, we must process all thing by ourselves
        else:
            sum_medals = get_sum_all_medals_in_query_with_group_by(result)
            if sum_medals < 20:
                continue
            relational_deviation = calculate_deviation_with_group_by(result, sum_medals)
        all_accepted_query.append(query)
        all_accepted_deviation.append(relational_deviation)

    # sort deviation
    index = all_accepted_deviation.index(max(all_accepted_deviation))
    print(bcolors.OKBLUE + "The Query with most relational deviation for part A of question 6 is : ")
    print(all_accepted_query[index])
    print("The value of relational deviations is : " + str(max(all_accepted_deviation)))


def get_sum_all_medals_in_query_with_group_by(records):
    medals = 0
    for item in records:
        medals += item[-1]
    return medals


def get_sum_all_medals_in_query_without_group_by(records):
    medals = 0
    all_per_record = []
    for item in records:
        sum_row = item[-1] + item[-2] + item[-3]
        medals += item[-1]
        medals += item[-2]
        medals += item[-3]
        all_per_record.append(sum_row)
    return medals, all_per_record


def calculate_deviation_with_group_by(records, sum_medals):
    sum_medals = float(sum_medals)
    avg = float(sum_medals/len(records))
    sigma = 0
    for rec in records:
        sigma += math.pow((float(rec[-1]) - avg), 2)
    sigma /= len(records)
    sigma = math.sqrt(sigma)
    sigma /= avg
    return sigma


def calculate_deviation_without_group_by(sum_medals, sum_per_record):
    sum_medals = float(sum_medals)
    avg = float(sum_medals/len(sum_per_record))
    sigma = 0
    for rec in sum_per_record:
        sigma += math.pow((float(rec) - avg), 2)
    sigma /= len(sum_per_record)
    sigma = math.sqrt(sigma)
    sigma /= avg
    return sigma


def get_most_ratio_medals_records(my_db):
    print(bcolors.OKGREEN + "Calculation Part B of Question 6 ...")
    my_cursor = my_db.cursor()
    all_accepted_query = []
    all_accepted_ratio = []
    for query in all_result_query:
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        if len(result) < 10:
            continue
        # do not have group by
        ratio_medal_record = 0
        if "GROUP" not in query:
            sum_medals, all_medal_per_record = get_sum_all_medals_in_query_without_group_by(result)
            ratio_medal_record = float(sum_medals) / float(len(result))
        # we do not have anything here, we must process all thing by ourselves
        else:
            sum_medals = get_sum_all_medals_in_query_with_group_by(result)
            ratio_medal_record = float(sum_medals) / float(len(result))
        all_accepted_query.append(query)
        all_accepted_ratio.append(ratio_medal_record)

    # sort deviation
    index = all_accepted_ratio.index(max(all_accepted_ratio))
    print(bcolors.OKBLUE + "The Query with most ratio of total medals to number of"
                           " records for part B of question 6 is : ")
    print(all_accepted_query[index])
    print("The value of ratio is : " + str(max(all_accepted_ratio)))


def get_most_in_progress_query(my_db):
    print(bcolors.OKGREEN + "Calculation Part C of Question 6 ...")
    my_cursor = my_db.cursor()
    all_accepted_query = []
    all_accepted_medals = []
    for query in all_result_query:
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        # do not have group by
        sum_medals = 0
        if "GROUP" not in query:
            sum_medals, ratio = get_sum_silver_bronze_medals_in_query_without_group_by(result)
        # we do not have anything here, we must process all thing by ourselves
        else:
            sum_medals, ratio = get_sum_silver_bronze_medals_in_query_with_group_by(result)
        if ratio >= 0.9:
            all_accepted_query.append(query)
            all_accepted_medals.append(sum_medals)

    # sort deviation
    index = all_accepted_medals.index(max(all_accepted_medals))
    print(bcolors.OKBLUE + "The Most Progressive Query is :")
    print(all_accepted_query[index])
    print("The number of medals is : " + str(max(all_accepted_medals)))


def get_sum_silver_bronze_medals_in_query_with_group_by(records):
    sum_all_medals = 0
    sum_bronze_silver = 0
    for item in records:
        sum_bronze_silver += item[-2]
        sum_bronze_silver += item[-3]
        sum_all_medals += item[-1]
    ratio = 0
    if sum_all_medals != 0:
        ratio = sum_bronze_silver / sum_all_medals
    return sum_all_medals, ratio


def get_sum_silver_bronze_medals_in_query_without_group_by(records):
    sum_all_medals = 0
    sum_bronze_silver = 0
    for item in records:
        sum_bronze_silver += item[-1]
        sum_bronze_silver += item[-2]
        sum_all_medals += item[-1]
        sum_all_medals += item[-2]
        sum_all_medals += item[-3]
    ratio = 0
    if sum_all_medals != 0:
        ratio = sum_bronze_silver / sum_all_medals
    return sum_all_medals, ratio


def get_most_developed_query(my_db):
    print(bcolors.OKGREEN + "Calculation Part D of Question 6 ...")
    my_cursor = my_db.cursor()
    all_accepted_query = []
    all_accepted_medals = []
    for query in all_result_query:
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        # do not have group by
        sum_medals = 0
        if "GROUP" not in query:
            sum_medals, ratio = get_sum_gold_medals_in_query_without_group_by(result)
        # we do not have anything here, we must process all thing by ourselves
        else:
            sum_medals, ratio = get_sum_gold_medals_in_query_with_group_by(result)
        if ratio >= 0.5:
            all_accepted_query.append(query)
            all_accepted_medals.append(sum_medals)

    # sort deviation
    index = all_accepted_medals.index(max(all_accepted_medals))
    print(bcolors.OKBLUE + "The Most Developed Query is :")
    print(all_accepted_query[index])
    print("The number of medals is : " + str(max(all_accepted_medals)))


def get_sum_gold_medals_in_query_with_group_by(records):
    sum_all_medals = 0
    sum_gold = 0
    for item in records:
        sum_gold += item[-4]
        sum_all_medals += item[-1]
    ratio = 0
    if sum_all_medals != 0:
        ratio = sum_gold / sum_all_medals
    return sum_all_medals, ratio


def get_sum_gold_medals_in_query_without_group_by(records):
    sum_all_medals = 0
    sum_gold = 0
    for item in records:
        sum_gold += item[-3]
        sum_all_medals += item[-1]
        sum_all_medals += item[-2]
        sum_all_medals += item[-3]
    ratio = 0
    if sum_all_medals != 0:
        ratio = sum_gold / sum_all_medals
    return sum_all_medals, ratio

