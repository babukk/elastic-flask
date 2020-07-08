
from pprint import pprint

from elasticsearch import Elasticsearch
import elasticsearch


class ElasticSearch(object):
    """ Класс для взаимодействия с ElasticSearch """

    def __init__(self, **kwargs):
        _host = kwargs.get('host')

        try:
            _port = int(kwargs.get('port'))
        except Ecxception as e:
            print("ElasticSearch::__init__: Port error: " + str(e))

        self.es = Elasticsearch([{'host': _host, 'port': _port, }])

    def getUser(self, _id):
        """ Получаем пользователя по его _id """
        user_info = None

        try:
            user_info = self.es.get(index='users', id=_id)
        except elasticsearch.exceptions.ConnectionError as e:
            print("ElasticSearch::getUser: Connection error: " + str(e))
        except elasticsearch.exceptions.NotFoundError as e:
            print("ElasticSearch::getUser: Not found error: " + str(e))

        try:
            return {'id': user_info['_id'], 'source': user_info['_source'], }
        except TypeError as e:
            print("ElasticSearch::getUsers: Undefined error: " + str(e))
            return {'id': None, 'source': None, }


    def getCompany(self, _id):
        """ Получаем компании по ее _id """
        comp_info = None

        try:
            comp_info = self.es.get(index='companies', id=_id)
        except elasticsearch.exceptions.ConnectionError as e:
            print("ElasticSearch::getCompany: Connection error: " + str(e))
        except elasticsearch.exceptions.NotFoundError as e:
            print("ElasticSearch::getCompany: Not found error: " + str(e))

        try:
            return {'id': comp_info['_id'], 'source': comp_info['_source'], }
        except TypeError as e:
            print("ElasticSearch::getCompany: Undefined error: " + str(e))
            return {'id': None, 'source': None, }

    def checkLoginExists(self, login):
        """ Проверка существования пользователя по логину """
        try:
            result = self.es.search(index='users', body={'query': {'prefix': {'login': login}}})
        except elasticsearch.exceptions.ConnectionError as e:
            print("ElasticSearch::checkLoginExists: Connection error: " + str(e))
        except elasticsearch.exceptions.NotFoundError as e:
            print("ElasticSearch::checkLoginExists: Not found error: " + str(e))

        try:
            if result['hits']['hits']:
                return True
            else:
                return False
        except TypeError as e:
            print("ElasticSearch::checkLoginExists: Undefined error: " + str(e))
            return False

        return

    def getUsers(self, _size=10000):
        """ Получаем список пользователей """
        users_list = []
        users_arr = []

        try:
            users_list = self.es.search(index='users', size=_size)
        except elasticsearch.exceptions.ConnectionError as e:
            print("ElasticSearch::getUsers: Connection error: " + str(e))
        except elasticsearch.exceptions.NotFoundError as e:
            print("ElasticSearch::getUsers: Not found error: " + str(e))

        try:
            for item in users_list['hits']['hits']:
                try:  users_arr.append({'id': item['_id'], 'source': item['_source'], })
                except Exception as e:
                    print("ElasticSearch::getUsers: " + str(e))
        except Exception as e:
            print("ElasticSearch::getUsers: " + str(e))

        return users_arr

    def getCompanies(self, _size=10000):
        """ Получаем список компаний """
        companies_list = []
        companies_arr = []

        try:
            companies_list = self.es.search(index='companies', size=_size)
        except elasticsearch.exceptions.ConnectionError as e:
            print("ElasticSearch::getCompanies: Connection error: " + str(e))
        except elasticsearch.exceptions.NotFoundError as e:
            print("ElasticSearch::getCompanies: Not found error: " + str(e))

        try:
            for item in companies_list['hits']['hits']:
                try:  companies_arr.append({'id': item['_id'], 'source': item['_source'], })
                except Exception as e:
                    print("ElasticSearch::getCompanies: " + str(e))
        except Exception as e:
             print("ElasticSearch::getCompanies: " + str(e))

        return companies_arr

    def addUser(self, **kwargs):
        """ Добавляем пользователя """
        fullname = kwargs.get('fullname')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        login = kwargs.get('login')
        avatar = kwargs.get('avatar')
        passwd = kwargs.get('passwd')
        position = kwargs.get('position')
        description = kwargs.get('description')

        try:
            new_user = self.es.index(
                index='users',
                body = {
                    'fullname': fullname,
                    'email': email,
                    'login': login,
                    'passwd': passwd,
                    'phone': phone,
                    'avatar': avatar,
                    'phone': phone,
                    'position': position,
                    'description': description,
                }
            )
        except elasticsearch.exceptions.ConnectionError as e:
            print("ElasticSearch::addUser: Connection error: " + str(e))
        except elasticsearch.exceptions.NotFoundError as e:
            print("ElasticSearch::addUser: Not found error: " + str(e))

        try:
            return new_user['_id']
        except TypeError as e:
            print("ElasticSearch::addUser: Undefined error: " + str(e))
            return None

    def addCompany(self, **kwargs):
        """ Добавляем компанию """
        city = kwargs.get('city')
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        description = kwargs.get('description')

        try:
            new_company = self.es.index(
                index='companies',
                body = {
                    'city': city,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'description': description,
                }
            )
        except elasticsearch.exceptions.ConnectionError as e:
            print("ElasticSearch::addCompany: Connection error: " + str(e))
        except elasticsearch.exceptions.NotFoundError as e:
            print("ElasticSearch::addCompany: Not found error: " + str(e))

