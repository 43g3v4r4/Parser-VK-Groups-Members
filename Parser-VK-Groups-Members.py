import requests
import json
import re
import time


access_token= 'Сервисный ключ доступа'
timeout = 1


with open("groupID.txt", "r") as file:#обрабатываем ссылки из файла для получения id сообществ
    lines = [line.rstrip('\n') for line in open('groupID.txt')]
    result_lines = []

    for i in lines:
        i = i.replace('https://vk.com/', '')
        i = i.replace('http://vk.com/', '')
        i = i.replace('https://www.vk.com/', '')
        i = i.replace('http://www.vk.com/', '')
        result_lines.append(i)

    groupsID = ','.join(result_lines)



def getgroupid(link):#получаем ID сообществ
    s = requests.Session()

    req = s.get('https://api.vk.com/method/groups.getById?group_ids=' + link + '&v=5.61&access_token=' + access_token).text
    results = json.loads(req)['response']
    list = []

    for i in results:
        list.append(i['id'])

    return list



for group_id in getgroupid(groupsID):#перебираем id сообществ и собираем их участников
    p = requests.Session()

    list_id = p.get('https://api.vk.com/method/groups.getMembers?group_id=' + str(group_id) + '&sort=id_asc&offset=0&count=1000&v=5.52&access_token=' + access_token).text
    totalResults = json.loads(list_id)["response"]["count"]

    pre_offset = round(totalResults / 1000)
    num_cycle = 0
    remains = 0
    ids = []

    for i in range(pre_offset):
        offset = str(i * 1000)
        list_id = p.get('https://api.vk.com/method/groups.getMembers?group_id=' + str(group_id) + '&sort=id_asc&offset=' + offset + '&count=1000&v=5.52&access_token=' + access_token).text
        id = json.loads(list_id)["response"]["items"]
        ids.extend(id)

        #Отчёт на экран
        num_cycle = num_cycle + 1
        remains = pre_offset - num_cycle

        print('Собираем в сообществе: ' + str(group_id) + ' - Осталось запросов: ' + str(remains))
        time.sleep(timeout)

    with open("result.txt", "a") as file:#пишим результат в файл result.txt
        print(*ids, file=file, sep="\n")

    print('Сообщество ' + str(group_id) + ' собрано.')


print('Все участники сообществ собраны!')