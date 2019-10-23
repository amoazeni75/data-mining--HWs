"""
Author: S.Alireza Moazeni
Student id : 9423110
Part 4
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn')

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

    # part c
    sql_query_ratio_country_medals = "SELECT country, count(id) as num_participants, " \
                                     "(SUM(gold) + SUM(bronze) + SUM(silver)) as total_medals, " \
                                     "((SUM(gold) + SUM(bronze) + SUM(silver)) / count(id)) as" \
                                     " ratio_participants_medals, (sum(gold) / count(id)) as gold_ratio," \
                                     " (sum(silver) / count(id)) as silver_ratio, (sum(bronze) / count(id))" \
                                     " as bronze_ration FROM `london12` group by country having num_participants > 29 order by ratio_participants_medals DESC LIMIT 0, 10"
    my_cursor.execute(sql_query_ratio_country_medals)
    result_ration_country_medals = my_cursor.fetchall()
    draw_bar_country_medal(result_ration_country_medals)



def draw_histogram_10_best_country(list_country):
    labels = []
    count_participants = []
    for tup in list_country:
        labels += (tup[1],)
        count_participants += (tup[0],)

    x = np.arange(0, len(labels) * 2, 2)  # the label locations
    width = 0.75 # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x, count_participants, width, align='center', label='Country', color='#3bb307')

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

    # row = 2
    # col = 4
    # fig, axs = plt.subplots(row, col)

    for index, item in enumerate(list_continent):
        fig1, axs = plt.subplots()
        axs.pie(medals[index], labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        axs.axis('equal')
        axs.set_title("Distribution of Medals in " + list_continent[index][0])
        plt.show()

    # # A standard pie plot
    # axs[0, 0].pie(medals[0], labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    # axs[0, 0].axis('equal')
    # axs[0, 0].set_title(list_continent[0][0])
    #plt.show()


def draw_bar_country_medal(country_list):
    country_name = []
    gold_ration = []
    silver_ration = []
    bronze_ration = []
    for tup in country_list:
        country_name.append(tup[0])
        gold_ration.append(round(tup[4], 2))
        silver_ration.append(round(tup[5], 2))
        bronze_ration.append(round(tup[6], 2))

    x = np.arange(0, len(country_name) * 2, 2)  # the label locations
    width = 0.35 # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, gold_ration, width, align='center', label='Ration of Participant to Gold Medals', color ='#d4af37')
    rects2 = ax.bar(x, silver_ration, width, align='center', label='Ration of Participant to Silver Medals', color= '#aaa9ad')
    rects3 = ax.bar(x + width, bronze_ration, width, align='center', label='Ration of Participant to Bronze Medals', color= '#cd7f32')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Medals\' Ration')
    ax.set_title('Ratio of participants to medals')
    ax.set_xticks(x)
    ax.set_xticklabels(country_name, rotation=80)
    ax.legend()
    auto_label(rects1, ax)
    auto_label(rects2, ax)
    auto_label(rects3, ax)
    fig.tight_layout()
    plt.show()