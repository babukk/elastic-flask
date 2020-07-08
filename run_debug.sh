#! /bin/sh
#----------------------------------------------------------------

HOME_DIR="."

cd ${HOME_DIR}
. ${HOME_DIR}/.venv3/bin/activate

python ./run_app.py --config-name=development --port=15000

# python test_elastic.py

deactivate
