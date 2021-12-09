from pymongo import MongoClient as msl
from pprint import pprint
client = msl('localhost', 27017)
db = client['instagram']
collection = db['instagramspider']
el1 = {'username': 'veralutik25', 'subscriber_on': True}    # Подписан на veralutik25
el2 = {'username': 'veralutik25', 'subscriber_on': False}    # На кого подписан veralutik25

def find_mongo(coll, elements):
    documents = coll.find(elements)
    documents = list(documents)
    len(documents)
    pprint(documents)


print('Список пользователей подписанных на veralutik25')
find_mongo(collection, el2)
"""
[{'_id': ObjectId('61b1e469eae26303244857a6'),
  'subscriber_avatar_link': 'https://instagram.fada1-11.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ad=z-m&_nc_ht=instagram.fada1-11.fna.fbcdn.net&_nc_cat=1&_nc_ohc=akN09iCy1aAAX8_bFcc&edm=ALlQn9MBAAAA&ccb=7-4&oh=006776c6870e5e0eda8e688edc97fb11&oe=61B7FE0F&_nc_sid=48a2a6&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4',
  'subscriber_id': 50363007003,
  'subscriber_link': 'http://instagram.com/vitalypython',
  'subscriber_login': 'vitalypython',
  'subscriber_name': 'Виталий Казанцев',
  'subscriber_on': False,
  'user_id': '29234179674',
  'username': 'veralutik25'},
  ...]
"""
print()
print('Список пользователей, на которых подписан(а) veralutik25')
find_mongo(collection, el1)
"""
[...
 {'_id': ObjectId('61b1e4d8eae2630324485903'),
  'subscriber_avatar_link': 'https://scontent-arn2-1.cdninstagram.com/v/t51.2885-19/s150x150/65302910_2322765234476793_3500578455693557760_n.jpg?_nc_ht=scontent-arn2-1.cdninstagram.com&_nc_cat=109&_nc_ohc=7T3HdrK-KDoAX-o3Y7o&edm=ALB854YBAAAA&ccb=7-4&oh=689669bedc5cf208a135cd5da0fcc59a&oe=61B87F5D&_nc_sid=04cb80',
  'subscriber_id': 7934758325,
  'subscriber_link': 'http://instagram.com/territoriitvorchestva',
  'subscriber_login': 'territoriitvorchestva',
  'subscriber_name': 'Территория Творчества Братск',
  'subscriber_on': True,
  'user_id': '29234179674',
  'username': 'veralutik25'},
....]
"""