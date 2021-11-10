"""
1. a) Посмотреть документацию к API GitHub,
   b) разобраться как вывести список репозиториев для конкретного пользователя,
   c) сохранить JSON-вывод в файле *.json.
2. a) Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
   b) Найти среди них любое, требующее авторизацию (любого типа).
   c) Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

import requests
import json
import environs

env = environs.Env()
env.read_env('.env')

