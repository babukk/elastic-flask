
import requests

#res = requests.get('http://172.9.0.6:9200')
#print(res.content)

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': '172.9.0.6', 'port': 9200}])

# xx = es.get(index='users', id='ODln6GkBZAe3JCUdtbM2')
zz = es.get(index='companies', id='OTlp6GkBZAe3JCUdrLM5')

print(zz)

"""
xx = es.search(index='users', body={'query': {'prefix': {'login': 'sadSD'}}})
print(xx['hits']['hits'])

if xx['hits']['hits']:
    print("found")
else:
    print("not found")
"""

# xx = es.get(index='users', id='VmrgM2oBoOXmBqtSJB_O')
# print(xx)

# print(zz)

#qq = es.delete(
#    index='users', id='WdvXLGoBCI87uvp_aDmJ'
#)

#print(qq)

#xx = es.search(index='companies')
# print(xx)


"""
qq = es.index(
    index='users',
    body={
        "passwd": "0000",
        "email": "tester111000@insitu.by",
        "login": "teste1999",
        "phone": "+700003223_9",
        "fullname": "Василий Пупкин 1999",
        "position": "tester1999",
        "avatar": "noimage",
        "description": "Тестер 1999"
    }
)

print(qq)
print(qq['_id'])
"""
"""
qq = es.index(
    index='companies',
    body={
        "city": "London",
        "phone": "435442345345",
        "name": "ООО ЯЯЯ",
        "description": "Компания #3",
        "email": "root001@mail.ru"
    }
)

print(qq)
"""
