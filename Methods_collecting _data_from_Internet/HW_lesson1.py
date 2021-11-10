#!/usr/bin/env python
# coding: utf-8

# # ДЗ Урока 1
# ## Казанцев Виталий
# 

# ### Задача 1. 
# * A Посмотреть документацию к API GitHub, 
# * B разобраться как вывести список репозиториев для конкретного пользователя, 
# * C сохранить JSON-вывод в файле *.json.
# 
# ### Задача 2. 
# * A Изучить список открытых API (https://www.programmableweb.com/category/all/apis). 
# * B Найти среди них любое, требующее авторизацию (любого типа). 
# * C Выполнить запросы к нему, пройдя авторизацию. 
# * D Ответ сервера записать в файл.

import requests
import json
import environs


env = environs.Env()
env.read_env('.env')

GITHUB_TOKEN = env('GITHUB_TOKEN')
USER_NAME = 'KazancevVitaly'
URL = f'https://api.github.com/users/{USER_NAME}/repos'

response = requests.get(URL)
r_json = response.json()

for rep in r_json:
    if not rep['private']:
        print(f'{r_json.index(rep)}{")"} {rep["name"]}')

with open('repos.json', 'w') as outfile:
    json.dump(r_json, outfile)

