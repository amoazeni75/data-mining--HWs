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

    # part b
    sql_query_get_medals = "SELECT continent, sum(gold), sum(silver), sum(bronze) FROM `london12` group by  continent"
    my_cursor.execute(sql_query_get_medals)
    result_continent_medals = my_cursor.fetchall()
    draw_circle_continent_medals(result_continent_medals)

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
    auto_label(rects1, ax)
    fig.tight_layout()
    plt.show()


def auto_label(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def draw_circle_continent_medals(list_continent):
    labels = ["Gold", "Silver", "Bronze"]
    medals = []
    for continent in list_continent:
        num_medals = continent[1] + continent[2] + continent[3]
        if num_medals == 0 :
            perc_medal = [0.0, 0.0, 0.0]
        else:
            perc_medal = [format((continent[1]/num_medals) * 100, '.4g'),
                          format((continent[2]/num_medals) * 100, '.4g'),
                          format((continent[3]/num_medals) * 100, '.4g')]
        medals.append(perc_medal)

    # fig1, ax1 = plt.subplots()
    # ax1.pie(medals[0], labels=labels, autopct='%1.1f%%',
    #         shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # ax1.set_title(list_continent[0][0])
    # plt.show()
    # Make figure and axes
    # row = 2
    # col = 4
    # fig, axs = plt.subplots(row, col)

    for index, item in enumerate(list_continent):
        fig1, axs = plt.subplots()
        axs.pie(medals[index], labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        axs.axis('equal')
        axs.set_title(list_continent[index][0])
        plt.show()

    # # A standard pie plot
    # axs[0, 0].pie(medals[0], labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    # axs[0, 0].axis('equal')
    # axs[0, 0].set_title(list_continent[0][0])

    #plt.show()