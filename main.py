# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import json

index = 0
productid_list = []
out_list = []
ID = []

phone_head_url = 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page='
phone_tail_url = '&s=217&click=0'

phoneid_head_url = 'https://sclub.jd.com/comment/productPageComments.action?&productId='
phoneid_middile_url = '&score=0&sortType=5&page='
phoneid_tail_url = '&pageSize=10&isShadowSku=0&fold=1'


def getID(url):
    for index in range(1, 2):
        re = requests.get(url)
        soup = BeautifulSoup(re.text, 'lxml')
        a_list = soup.find_all('li', class_='gl-item')
        for item in a_list:
            productid = item['data-pid']
            productid_list.append(productid)
    return productid_list


def getComment(url):
    for index in range(1, 100):
        re = requests.get(url)
        soup = BeautifulSoup(re.text, 'lxml')
        if re.status_code == 200:
            origin_data = re.text
            strBe = origin_data.find('(')
            data = origin_data[strBe+1:-2]
            json_data = json.loads(data, encoding="utf - 8")
            comments = json_data["comments"]
            for item in comments:
                content = item['content']
                time = item['creationTime']
                score = item['score']
                user_level = item["userLevelName"]
                name = item['nickname']
                new_item = {'name': name, 'level': user_level,
                            'socre': score, 'time': time, 'comment': content}
                out_list.append(new_item)
    return out_list

def getallID() :
    for index in range(1, 2):
        phone_url = phone_head_url + str(index) + phone_tail_url
        id = getID(phone_url)
        ID.append(id)
    return ID

def flatten(input_list):
    output_list = []
    while True :
        if input_list == []:
            break
        for index , i in enumerate(input_list):
            if type(i) == list :
                input_list = i + input_list[index+1:]
                break
            else :
                output_list.append(i)
                input_list.pop(index)
                break

    return output_list
            
originID = getallID()
finalID = flatten(originID)

for i in finalID:
    phoneid_origin_url = phoneid_head_url + str(i) + phoneid_middile_url
    for index in range(1, 100):
        phoneid_url = phoneid_origin_url + str(index) + phoneid_tail_url
        comment = getComment(phoneid_url)
        comment = json.dumps(comment, ensure_ascii=False)
        file = open('data.json', 'w', encoding='utf-8')
        file.write(comment)
        file.close()
