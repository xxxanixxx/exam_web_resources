import numpy as np
from flask import Flask, render_template, request
import requests
import json
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from bs4 import BeautifulSoup
import math


# app = Flask(__name__)


# def most_19_18_17(years, list_most, r, flag_on_website):
#     if years in '2019':
#         list_most.append(float(r.find_all('div')[1].text.replace('%', "")))
#         flag_on_website = True
#     else:
#         list_most.append(float(r.find('span').text.replace('%', "")))
#         flag_on_website = True
#     return list_most, flag_on_website
#
#
# def most_ldw_191817(years, result_section, technology, list_most, flag_on_website):
#     for bar_set in result_section:
#         bar_row = bar_set.find_all('div', {'class': 'bar-row'})
#         for r in bar_row:
#             result_technology = r.find_all('div')[0].text.lower()
#             if result_technology == technology:
#                 list_most_loved, flag_on_website = most_19_18_17(years, list_most, r,  flag_on_website)
#             if flag_on_website:
#                 break
#         if flag_on_website:
#             # flag_on_website = False
#             break
#     return list_most, flag_on_website
#
#
# def most_loved_dreaded_wanted_2020(tr, technology, list_most, flag_on_website):
#     tr = tr.find_all('tr')
#     for r in tr:
#         result_technology = r.find_all('td')[0].text.lower().replace("\r", ""). \
#             replace("\n", "").replace(" ", "")
#         if result_technology == technology.replace(" ", ""):
#             list_most.append(float(r.find_all('td')[1].find('span').text.replace("%", "")))
#             flag_on_website = True
#             break
#     return list_most, flag_on_website
#
#
# # @app.route("/")
# # def home():
# #     return render_template('home.html')
# #
#
# @app.route("/help")
# def help():
#     return render_template('help.html')
#
#
# @app.route("/about")
# def about():
#     return render_template('about.html')
#
#
# @app.route("/result", methods=['POST'])
# def result():



def most_19_18_17(years, list_most, r, flag_on_website):
    if years in '2019':
        list_most.append(float(r.find_all('div')[1].text.replace('%', "")))
        flag_on_website = True
    else:
        list_most.append(float(r.find('span').text.replace('%', "")))
        flag_on_website = True
    return list_most, flag_on_website


def most_ldw_191817(years, result_section, technology, list_most, flag_on_website):
    for bar_set in result_section:
        bar_row = bar_set.find_all('div', {'class': 'bar-row'})
        for r in bar_row:
            result_technology = r.find_all('div')[0].text.lower()
            if result_technology == technology:
                list_most, flag_on_website = most_19_18_17(years, list_most, r, flag_on_website)
            # if technology in result_technology:
            #     if result_technology == technology:
            #         list_most, flag_on_website = most_19_18_17(years, list_most, r,  flag_on_website)
            #     elif years in '2018':
            #         if len(technology) / len(result_technology) > 0.279 and len(technology) < len(result_technology):
            #             list_most.append(float(r.find('span').text.replace('%', "")))
            #             flag_on_website = True
            #     elif years in '2017':
            #         if (len(technology) / len(result_technology) > 0.46 and len(technology) < len(result_technology)) \
            #                 or technology in ('(' + result_technology + ')'):
            #             list_most.append(float(r.find('span').text.replace('%', "")))
            #             flag_on_website = True

                # print(flag_on_website)
            if flag_on_website:
                break
        if flag_on_website:
            # flag_on_website = False
            break
    return list_most, flag_on_website


def most_loved_dreaded_wanted_2020(tr, technology, list_most, flag_on_website):
    tr = tr.find_all('tr')
    for r in tr:
        result_technology = r.find_all('td')[0].text.lower().replace("\r", ""). \
            replace("\n", "").replace(" ", "")
        if result_technology == technology.replace(" ", ""):
            list_most.append(float(r.find_all('td')[1].find('span').text.replace("%", "")))
            flag_on_website = True
            break
    return list_most, flag_on_website

list_years = ['2022', '2021', '2020', '2019', '2018', '2017']
list_most_popular = []
list_most_loved = []
list_most_dreaded = []
list_most_wanted = []
list_top_paying = []
technology = ""
flag_on_website = False

technology = 'JavaScript'.lower()

for years in list_years:
    if years in '2022':
        url_years = 'https://survey.stackoverflow.co/' + years
    else:
        url_years = 'https://insights.stackoverflow.com/survey/' + years

    response = requests.get(url_years)
    soup = BeautifulSoup(response.text, "html.parser")
    result_section = soup.find('section', {'id': 'technology'})

    if years in '2022' or years in '2021':

        result_section_most_popular = result_section.find('section',
                                                          {'id': 'technology-most-popular-technologies'})
        result_section_most_loved_dreaded_wanted = result_section.find('section', {
            'id': 'technology-most-loved-dreaded-and-wanted'})
        result_section_top_paying = result_section.find('section', {'id': 'technology-top-paying-technologies'})

        result_section_most_popular = result_section_most_popular.find_all('article')
        result_section_most_loved_dreaded_wanted = result_section_most_loved_dreaded_wanted.find_all('article')
        result_section_top_paying = result_section_top_paying.find('article')

        for rs in result_section_most_popular:
            tr = rs.find_all('div')[2]
            tr = tr.find_all('figure')[0]
            tr = tr.find_all('tr')
            if rs == result_section_most_popular[-1] and years == '2022':
                list_result_technology = []
                list_result_percent_platforms = []
                for i in range(0, 15, 3):
                    list_result_technology.append(tr[i].find('span').text.lower())
                    list_result_percent_platforms.append(
                        round(((float(tr[i + 1].find('span').text.replace("%", "")) +
                                float(tr[i + 2].find('span').text.replace("%", ""))) / 2), 2))
                for i in range(len(list_result_technology)):
                    if list_result_technology[i] == technology:
                        list_most_popular.append(list_result_percent_platforms[i])
                        flag_on_website = True
                        break
                if flag_on_website:
                    # flag_on_website = False
                    break
            else:
                for r in tr:
                    result_technology = r.find_all('td')[0].text.lower()
                    if result_technology == technology:
                        list_most_popular.append(float(r.find_all('td')[1].find_all('span')[0].text.
                                                       replace(" ", "").replace("%", "")))
                        flag_on_website = True
                        break
                if flag_on_website:
                    # flag_on_website = False
                    break
        if not flag_on_website:
            list_most_popular.append("")
        else:
            flag_on_website = False

        for art in result_section_most_loved_dreaded_wanted:
            art = art.find_all('div')[2]
            fig_loved_dreaded = art.find_all('figure')[0]

            if years == '2022':
                fig_loved_dreaded = fig_loved_dreaded.find_all('div')[2]

            else:
                fig_loved_dreaded = fig_loved_dreaded.find_all('div')[1]

            fig_loved_dreaded = fig_loved_dreaded.get('data-json')
            data_json = json.loads(fig_loved_dreaded)

            list_json_technology = []
            list_json_loved = []
            list_json_dreaded = []

            for list_jsn in data_json:
                list_json_technology.append(list_jsn['response'].lower())
                list_json_loved.append(round(float(list_jsn['percent1']) * 100, 2))
                list_json_dreaded.append(round(float(list_jsn['percent2']) * 100, 2))

            for i in range(len(list_json_technology)):
                if list_json_technology[i] == technology:
                    list_most_loved.append(list_json_loved[i])
                    list_most_dreaded.append(list_json_dreaded[i])
                    flag_on_website = True
                    break

            fig_wanted = art.find_all('figure')[1]
            fig_wanted = fig_wanted.find_all('tr')
            for r in fig_wanted:
                result_technology = r.find_all('td')[0].text.lower()
                if result_technology == technology:
                    list_most_wanted.append(float(r.find_all('td')[1].find('span').text.replace(" ", "").
                                            replace("%", "")))
                    # flag_on_website = True
                    break
        if not flag_on_website:
            list_most_loved.append("")
            list_most_dreaded.append("")
            list_most_wanted.append("")
        else:
            flag_on_website = False


        result_section_top_paying = result_section_top_paying.find_all('div')[2]
        result_section_top_paying = result_section_top_paying.find_all('figure')
        for fig in result_section_top_paying:
            fig = fig.find_all('tr')
            for tr in fig:
                result_technology = tr.find_all('td')[0].text.lower()
                if result_technology == technology:
                    list_top_paying.append((int(tr.find_all('td')[1].find('span').text
                                                .replace(",", "").replace(" ", "").replace("$", "")) * 71)/1000)
                    flag_on_website = True
                    break
            if flag_on_website:
                # flag_on_website = False
                break
        if not flag_on_website:
            list_top_paying.append("")
        else:
            flag_on_website = False

    elif years in '2020':

        result_section_most_popular = result_section.find('div', {'id': 'most-popular-technologies'})
        result_section_most_loved_dreaded_wanted = result_section.find('div',
                                                                       {'id': 'most-loved-dreaded-and-wanted'})
        result_section_top_paying = result_section.find('div', {'id': 'top-paying-technologies'})

        result_section_most_popular = result_section_most_popular.find_all('article')
        result_section_most_loved_dreaded_wanted = result_section_most_loved_dreaded_wanted.find_all('article')
        result_section_top_paying = result_section_top_paying.find('article')

        for art in result_section_most_popular:
            art = art.find_all('div')[2]
            art = art.find_all('tr')
            for r in art:
                result_technology = r.find_all('td')[0].text.lower().replace("\r", "").\
                    replace("\n", "").replace(" ", "")
                if result_technology == technology.replace(" ", ""):
                    list_most_popular.append(float(r.find_all('td')[1].find('span').text.replace('%', "")))
                    flag_on_website = True
                    break
            if flag_on_website:
                # flag_on_website = False
                break

        if not flag_on_website:
            list_most_popular.append("")
        else:
            flag_on_website = False

        for art in result_section_most_loved_dreaded_wanted:
            art = art.find_all('div')[2:5]
            for tr in art:
                if tr == art[0]:
                    list_most_loved, flag_on_website = most_loved_dreaded_wanted_2020\
                        (tr, technology, list_most_loved, flag_on_website)
                    # if flag_on_website:
                    #     flag_on_website = False
                        # continue

                elif tr == art[1]:
                    list_most_dreaded, flag_on_website = most_loved_dreaded_wanted_2020\
                        (tr, technology, list_most_dreaded, flag_on_website)
                    # if flag_on_website:
                    #     flag_on_website = False
                        # continue
                else:
                    list_most_wanted, flag_on_website = most_loved_dreaded_wanted_2020\
                        (tr, technology, list_most_wanted, flag_on_website)
                    # if flag_on_website:
                    #     flag_on_website = False
                        # continue
            if flag_on_website:
                break

        if not flag_on_website:
            list_most_loved.append("")
            list_most_dreaded.append("")
            list_most_wanted.append("")
        else:
            flag_on_website = False


        # if len(list_most_loved) > len(list_most_dreaded):
        #     list_most_dreaded.append(round(100 - list_most_loved[-1], 1))
        # elif len(list_most_loved) < len(list_most_dreaded):
        #     list_most_loved.append(round(100 - list_most_dreaded[-1], 1))



        result_section_top_paying = result_section_top_paying.find_all('div')[2]
        result_section_top_paying = result_section_top_paying.find_all('tr')
        for r in result_section_top_paying:
            result_technology = r.find_all('td')[0].text.lower().replace("\r", "").replace("\n", "").\
                replace(" ", "")
            if result_technology == technology.replace(" ", ""):
                list_top_paying.append((int(r.find_all('td')[1].find('span').text
                                            .replace("k", "000").replace("$", "")) * 72)/1000)
                flag_on_website = True
                break
        if not flag_on_website:
            list_top_paying.append("")
        else:
            flag_on_website = False

    else:
        result_section = result_section.find('div', {'class': 'section-content'})
        if years in '2019':
            result_section_most_popular = result_section.find_all('div', {'class': 'bar-set'})[0:10:2]
            result_section_most_loved = result_section.find_all('div', {'class': 'bar-set'})[10:25:3]
            result_section_most_dreaded = result_section.find_all('div', {'class': 'bar-set'})[11:25:3]
            result_section_most_wanted = result_section.find_all('div', {'class': 'bar-set'})[12:25:3]
            result_section_top_paying = result_section.find_all('div', {'class': 'bar-set'})[34]
        elif years in '2018':
            result_section_most_popular = result_section.find_all('div', {'class': 'bar-set'})[0:8:2]
            result_section_most_loved = result_section.find_all('div', {'class': 'bar-set'})[8:20:3]
            result_section_most_dreaded = result_section.find_all('div', {'class': 'bar-set'})[9:20:3]
            result_section_most_wanted = result_section.find_all('div', {'class': 'bar-set'})[10:20:3]
            result_section_top_paying = result_section.find_all('div', {'class': 'bar-set'})[27]
        else:
            result_section_most_popular = result_section.find_all('div', {'class': 'bar-set'})[1:12:3]
            result_section_most_loved = result_section.find_all('div', {'class': 'bar-set'})[12:24:3]
            result_section_most_dreaded = result_section.find_all('div', {'class': 'bar-set'})[13:24:3]
            result_section_most_wanted = result_section.find_all('div', {'class': 'bar-set'})[14:24:3]
            result_section_top_paying = result_section.find_all('div', {'class': 'bar-set'})[32]

        for bar_set in result_section_most_popular:
            bar_row = bar_set.find_all('div', {'class': 'bar-row'})
            for r in bar_row:
                result_technology = r.find_all('div')[0].text.lower()
                if result_technology == technology:
                    list_most_popular, flag_on_website = most_19_18_17(years, list_most_popular, r,
                                                                       flag_on_website)
                # if technology in result_technology:
                #     if result_technology == technology:
                #         list_most_popular, flag_on_website = most_19_18_17(years, list_most_popular, r,
                #                                                            flag_on_website)
                #     elif years in '2018':
                #         if len(technology) / len(result_technology) > 0.279:
                #             list_most_popular.append(float(r.find('span').text.replace('%', "")))
                #             flag_on_website = True
                #             break
                #     elif years in '2017':
                #         if len(technology) / len(result_technology) > 0.46 or technology in (
                #                 '(' + result_technology + ')'):
                #             list_most_popular.append(float(r.find('span').text.replace('%', "")))
                #             flag_on_website = True
                #             break

        if not flag_on_website:
            list_most_popular.append('')
        else:
            flag_on_website = False

        list_most_loved, flag_on_website = most_ldw_191817(years, result_section_most_loved, technology,
                                                           list_most_loved, flag_on_website)
        list_most_dreaded, flag_on_website = most_ldw_191817(years, result_section_most_dreaded, technology,
                                                             list_most_dreaded, flag_on_website)

        if len(list_most_loved) > len(list_most_dreaded):
            list_most_dreaded.append(round(100 - float(list_most_loved[-1]), 1))
        elif len(list_most_loved) < len(list_most_dreaded):
            list_most_loved.append(round(100 - float(list_most_dreaded[-1]), 1))

        if not flag_on_website:
            list_most_loved.append('')
            list_most_dreaded.append('')
        else:
            flag_on_website = False

        list_most_wanted, flag_on_website = most_ldw_191817(years, result_section_most_wanted, technology,
                                                            list_most_wanted, flag_on_website)
        if not flag_on_website:
            list_most_wanted.append('')
        else:
            flag_on_website = False

        bar_row = result_section_top_paying.find_all('div', {'class': 'bar-row'})
        for r in bar_row:
            result_technology = r.find_all('div')[0].text.lower()
            if result_technology == technology:
                if years in '2019':
                    list_top_paying.append((int(r.find_all('div')[1].text.replace("k", "000").replace("$", ""))
                                            * 65)/1000)
                    flag_on_website = True
                    break
                else:
                    list_top_paying.append((int(r.find('span').text.replace(",", "").replace("$",""))
                                            * 60)/1000)
                    flag_on_website = True
                    break
        if not flag_on_website:
            list_top_paying.append("")
        else:
            flag_on_website = False


print(list_most_popular)
print(list_most_loved)
print(list_most_dreaded)
print(list_most_wanted)
print(list_top_paying)
if list_most_popular[:] == '' and list_most_loved[:] == '' and list_most_dreaded[:] == '' \
            and list_most_wanted[:] == '' and list_top_paying[:] == '':
    print('jhkhh')
# print(sum(list_most_popular))
# print(sum(list_most_loved))
# print(sum(list_most_dreaded))
# print(sum(list_most_wanted))
# print(sum(list_top_paying))
# print(list_most_popular[:]/sum())


# if not (list_most_popular and list_most_loved and list_most_dreaded and list_most_wanted and list_top_paying):
#     return render_template('result.html',  list_most_popular=list_most_popular, list_most_loved=list_most_loved,
#                            list_most_dreaded=list_most_dreaded, list_most_wanted=list_most_wanted,
#                            list_top_paying=list_top_paying, technology=technology)
pictures = []
y1 = []
y2 = []
y3 = []
y4 = []
# y_plot = []
# list_years_plot = []
for i in range(4):
    y_plot = []
    list_years_plot = []
    if i == 0:
        for j in range(len(list_most_popular)):
            if list_most_popular[j] != '':
                y_plot.append(list_most_popular[j])
                list_years_plot.append(list_years[j])
    elif i == 1:
        for j in range(len(list_most_loved)):
            if list_most_loved[j] != '':
                y_plot.append(list_most_loved[j])
                list_years_plot.append(list_years[j])
    elif i == 2:
        for j in range(len(list_most_dreaded)):
            if list_most_dreaded[j] != '':
                y_plot.append(list_most_dreaded[j])
                list_years_plot.append(list_years[j])
    elif i == 3:
        for j in range(len(list_most_wanted)):
            if list_most_wanted[j] != '':
                y_plot.append(list_most_wanted[j])
                list_years_plot.append(list_years[j])
    if len(y_plot) != 0:
        # print(y)
        # plt.switch_backend('Agg')
        fig = plt.figure()
        # if len(y) < len(list_years):
        #     plt.plot(list_years[:], y)
        # else:
        #     plt.plot(list_years, y)
        # list_years_plot =[]
        # y_plot = []
        # for y_i in range(len(y)):
        #     if y[y_i] != '':
        #         list_years_plot.append(list_years[y_i])
        #         y_plot.append(y[y_i])
        minimum = min(y_plot)
        maximum = max(y_plot)
        plt.plot(list_years_plot, y_plot, 'b', y_plot, 'bo')
        plt.plot(list_years_plot, [sum(y_plot)/len(y_plot) for i in range(len(y_plot))], 'r--')
        plt.legend(['?????????????????? %', '% ?? ????????', '?????????????? % \n' + str(round(sum(y_plot)/len(y_plot), 2))], loc=0)
        plt.grid()
        plt.xlabel('????????', color='blue')
        # buf = BytesIO()
        if i == 0:
            plt.ylabel('% ????????????????????????', color='blue')
        elif i == 1:
            plt.ylabel('% ????????????????????????????????????', color='blue')
        elif i == 2:
            plt.ylabel('% ??????????????????????????', color='blue')
        elif i == 3:
            plt.ylabel('% ????????????????????????????????????', color='blue')

        plt.yticks(np.arange(math.floor(minimum), math.ceil(maximum) + 1, step=0.7))

        # fig.savefig(buf, format='png')
        # pictures.append(base64.b64encode(buf.getbuffer()).decode('ascii'))
        plt.show()
    else:
        y_empty = '???? ???? ???????????? ?????????????????? ????????????. ???????????? ???? 2022-2017 ????. ??????????????????????. '


pictures = []
fig = plt.figure()
# list_years_plot =[]
list_years_plot1 = []
list_years_plot2 = []
list_years_plot3 = []
list_years_plot4 = []
y_plot1 = []
y_plot2 = []
y_plot3 = []
y_plot4 = []
for i in range(len(list_most_popular)):
    if list_most_popular[i] != '':
        y_plot1.append(list_most_popular[i])
        list_years_plot1.append(list_years[j])
for i in range(len(list_most_loved)):
    if list_most_loved[i] != '':
        y_plot2.append(list_most_loved[i])
        list_years_plot2.append(list_years[j])
for i in range(len(list_most_dreaded)):
    if list_most_dreaded[i] != '':
        y_plot3.append(list_most_dreaded[i])
        list_years_plot3.append(list_years[j])
for i in range(len(list_most_wanted)):
    if list_most_wanted[i] != '':
        y_plot4.append(list_most_wanted[i])
        list_years_plot4.append(list_years[j])
print(len(y_plot1))
print(len(y_plot2))
print(len(y_plot3))
print(len(y_plot4))

print(np.array_equal(list_years_plot1, list_years_plot2))
print(np.array_equal(list_years_plot1, list_years_plot3))
print(np.array_equal(list_years_plot1, list_years_plot4))
print(np.array_equal(list_years_plot2, list_years_plot3))
print(np.array_equal(list_years_plot2, list_years_plot4))
print(np.array_equal(list_years_plot3, list_years_plot4))

print(list_years)
print(list_years_plot1)
print(list_years_plot2)
print(list_years_plot3)
print(list_years_plot4)



if y_plot1[:] != '' and y_plot2[:] != '' and y_plot3[:] != '' and y_plot4[:] != '':
    minimum = min(min(y_plot1), min(y_plot2), min(y_plot3), min(y_plot4))
    maximum = max(max(y_plot1), max(y_plot2), max(y_plot3), max(y_plot4))
    plt.plot(list_years, y_plot1, color='indigo')
    plt.plot(list_years, y_plot2, 'r')
    plt.plot(list_years, y_plot3, 'b')
    plt.plot(list_years, y_plot4, 'g')
    plt.yticks(np.arange(math.floor(minimum), math.ceil(maximum) + 5, step=5))
    plt.grid()
    plt.xlabel('????????', color='blue')
    plt.ylabel('% ?? ??????????????????', color='blue')
    plt.legend(['????????????????????????', '?????????????? ?? ??????????????????????', '??????????????????????????', '????????????????????????????????????'], loc=0, fontsize=5)
    plt.show()
else:
    y_empty = '???? ???? ???????????? ?????????????????? ????????????. ???????????? ???? 2022-2017 ????. ??????????????????????. '

# picture_bar = []
y = []
y_plot = []
list_years_plot = []
for j in range(len(list_top_paying)):
    if list_top_paying[j] != '':
        y_plot.append(list_top_paying[j])
        list_years_plot.append(list_years[j])
if len(y_plot) != 0:
    fig = plt.figure()
    minimum = min(y_plot)
    maximum = max(y_plot)
    plt.bar(list_years_plot, y_plot)
    plt.plot(list_years_plot, [sum(y_plot) / len(y_plot) for i in range(len(y_plot))], 'r--')
    # plt.grid(color='grey', linestyle='dashed')
    plt.xlabel('????????', color='blue')
    plt.ylabel('?????????????? ?????????????????? ?? ??????. ????????.', color='blue')
    for i in range(len(list_years_plot)):
        plt.text(list_years_plot[i], 300, '{:.1f}'.format(y_plot[i]), color='r')
    plt.yticks(np.arange(0, math.ceil(maximum) + 1000, step=300), np.arange(0, math.ceil(maximum) + 1000, step=300))
    plt.legend(['?????????????? ?????????????????? ???? ?????????? \n' + str(round(sum(y_plot)/len(y_plot), 2))])
    # plt.pie(y_plot, labels=list_years_plot, explode=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06][:len(y_plot)],
    #         autopct= lambda p: '{:.1f} ??????.'.format(p * sum(y_plot) / 100), pctdistance=0.65)
    # plt.title('?????????????? ?????????????????? ???? ????????, ??????. ????????????', color='b')
    plt.show()
