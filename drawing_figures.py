"""
Author: S.Alireza Moazeni
Student id : 9423110
Part 4
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def get_draw_statistics(my_db):
    # part a
    my_cursor = my_db.cursor()
    sql_query_get_top_10 = "SELECT COUNT(id), country FROM `london12` GROUP BY country ORDER by COUNT(id) DESC LIMIT 0, 10"
    my_cursor.execute(sql_query_get_top_10)
    result_10_country = my_cursor.fetchall()
    draw_histogram_10_best_country(result_10_country)



def draw_histogram_10_best_country(list_country):
    labels = []
    count_participants = []
    for tup in list_country:
        labels += (tup[1],)
        count_participants += (tup[0],)

    x = np.arange(0, len(labels) * 2, 2)  # the label locations
    width = 0.75 # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x, count_participants, width, align='center', label='Country', color = [(0, 1.0, 1.0)])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of Participants')
    ax.set_title('Number of Participants in a Country')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=80)
    ax.legend()
    autolabel(rects1, ax)
    fig.tight_layout()
    plt.show()


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')