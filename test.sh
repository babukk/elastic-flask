#! /bin/sh
#----------------------------------------------------------------

HOME_DIR="."

cd ${HOME_DIR}
. ${HOME_DIR}/.venv3/bin/activate

python test_elastic.py

deactivate
