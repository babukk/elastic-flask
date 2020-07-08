#! /bin/sh
#----------------------------------------------------------------

HOME_DIR="."

cd ${HOME_DIR}
virtualenv -p `which python3` .venv3
. ${HOME_DIR}/.venv3/bin/activate

pip install -r requirements.txt

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

deactivate
