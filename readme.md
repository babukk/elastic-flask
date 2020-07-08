```
sudo apt install libaprutil1-dev

HOME_DIR="/home/elastic/_project/es"  (для примера)

$ cd ${HOME_DIR}
$ virtualenv -p `which python3` .venv3

$ . ${HOME_DIR}/.venv3/bin/activate

(.venv3) $ pip install -r requirements.txt

(.venv3) $ python manage.py db init
(.venv3) $ python manage.py db migrate
(.venv3) $ python manage.py db upgrade

В ./secret/.htpasswd создаем учетную запись (суперпользователя):
$ htpasswd -c /secret/.htpasswd root

Параметры подключения БД mysql, ElasticSearch и т.п.):
./instance/config.py

Запуск в debug-mode:
./run_debug.sh

Для запуска в production рекомендуется связка nginx + uwsgi-emperor:
sudo apt install nginx uwsgi-emperor uwsgi-plugin-pythoh

Пример ini-файла для uwsgi-emperor:
./deploy/etc/uwsgi-emperor/vassals/es.ini

Пример conf-файла для nginx:
./deploy/etc/nginx/sites-available/es.conf
и symbolic-линк:
./deploy/etc/nginx/sites-enable/es.conf -> ../sites-available/es.conf

Для перезапуска:
systemctl restart uwsgi-emperor
systemctl restart nginx

```