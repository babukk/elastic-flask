
SECRET_KEY = 'p9Bv<3Eid9%$i07'

SQLALCHEMY_DATABASE_URI = "sqlite://///home/elastic/_project/es/_db/users.db"

SQLALCHEMY_BINDS = {
    'DEV_DB': 'mysql+pymysql://es_dev:x123456z@localhost/dev-db',
}

FLASK_HTPASSWD_PATH = '/home/elastic/_project/es/secret/.htpasswd'

ELASTIC_HOST = "172.9.0.10"
ELASTIC_PORT = "9200"
