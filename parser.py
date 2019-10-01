# -*- coding: utf-8 -*-
import requests
import json
import time
from tqdm import tqdm
from datetime import datetime
import os


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


colors = {0: "#ffebeb", 1: "#e8fff0", 2: "#edeeff", 3: "#fffdf7", 4: "#f0feff"}
data = requests.get("https://www.dpomos.ru/api/getCurrentCoursesId").json()
# print(data)
print('Начало периода (формат гггг-мм-дд):')
begin = input()
print('Конец периода (формат гггг-мм-дд):')
end = input()
# begin = '2019-09-06'
# end = '2019-10-08'
i = 1
html = '<table  style="width: 100%;" cellspacing="1" cellpadding="1" border="0"><tbody><tr><td style="text-align: center; width: 160px; vertical-align: top; background-color: #f2f2f2;"><p><strong><em>Дата</em></strong></p></td><td style="text-align: center; width: 160px; vertical-align: top; background-color: #f2f2f2;"><p style="text-align: center;"><em style="text-align: center;"><strong>Шифр</strong></em></p></td><td style="text-align: center; width: 160px; vertical-align: top; background-color: #f2f2f2;"><p><em style="text-align: center;"><strong>Название</strong></em></p></td><td style="text-align: center; width: 160px; vertical-align: top; background-color: #f2f2f2;"><p><em><strong>Портал&nbspДПО</strong></em></p></td></tr>'
courseArray = []
courseDate = []
course = []
# courseMcrkpoCount = sum(1 for d in data if d['departaments'] == 'ГАОУ ДПО МЦРКПО')
print("Всего курсов на dpomos.ru: " + str(len(data)))
print("Дождитесь загрузки...")
# print(courseMcrkpoCount)
orgName = 'МЦРКПО'
# orgName = orgName.decode("utf-8")
l = len(data)

printProgressBar(0, l, prefix='Завершено на:', suffix='', length=50)
for val in data:

    course += requests.get("https://www.dpomos.ru/api/getCourseById?id=" + val).json()
    time.sleep(0.1)
    # Update Progress Bar
    printProgressBar(i + 1, l, prefix='Завершено на:', suffix='', length=50)
    i = i + 1
    # if i > 100:
    #     break

for val in course:
    if val['date_group_starts'] is not None and orgName in val['departaments'] and '-Д' not in val['code']:
        for v in val['date_group_starts']:
            if begin <= v['from'] <= end:
                courseDate.append(v['from'])

for val in course:
    # print(val['departaments'])
    if val['date_group_starts'] is not None and orgName in val['departaments'] and '-Д' not in val['code']:
        for v in val['date_group_starts']:
          if v['from'] in courseDate:
              # print(val['departaments'])
              c = {'date': v['from'], 'code': val['code'], 'name': val['name'], 'departaments': val['departaments'], 'link': 'https://www.dpomos.ru/curs/' + val['id']}
              courseArray.append(c)


# print(courseDate)
courseList = sorted(set(courseDate))
# print(courseList)
colorCounter = 0
for val in courseList:
    numberOfCoursesOnDate = sum(1 for i in courseArray if i['date'] == val)
    valDate = datetime.date(datetime.strptime(val, '%Y-%m-%d'))
    html += "<tr ><td rowspan=\"" + str(numberOfCoursesOnDate) + "\" style=\"background-color:" + colors[colorCounter] + "; text-align: center; vertical-align: top;\"><p><strong>" + str("{:02d}".format(valDate.day)) + "." + str("{:02d}".format(valDate.month)) + "." + str(valDate.year) + "</strong></p></td>"
    numberOfString = 1

    for v in courseArray:
        if v['date'] == val:
            if numberOfString != 1:
                html += "<tr>"
            html += "<td " \
                    "style=\"background-color:" + colors[colorCounter] + "; text-align: center; vertical-align: top;\"><p><strong>" + v['code'] + "</strong></p></td>" + \
                    "<td " \
                    "style=\"background-color:" + colors[colorCounter] + "; vertical-align: top;\"><p>" + v['name'] + "</p></td>" + \
                    "<td " \
                    "style=\"background-color:" + colors[colorCounter] + "; text-align: center; vertical-align: top;\"><p><a class=\"btn btn-success\" href=\"" + v['link'] + "/#card\" target=\"_blank\">Записаться</a></p></td>" + \
                    "</tr>"
            numberOfString += 1
    if colorCounter == len(colors) - 1:
        colorCounter = 0
    else:
        colorCounter += 1

html += '</tbody></table>'
filename = "Ближайшие курсы на " + datetime.now().strftime("%Y_%m_%d-%H-%M-%S") + ".html"

f = open(filename, 'w', encoding='utf-8')

print(html, file=f)
f.close()
print("Где-то рядом лежит файлик " + filename + ", там табличка.")
os.system('pause')
