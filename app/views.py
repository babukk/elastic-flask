
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func
from sqlalchemy import exc
# import sqlalchemy
from aprmd5 import password_validate
import json
from pprint import pprint
import hashlib

from . import app, db, db_es, login_manager
from . models import User, LoginForm, UserCompanyRel, UserRoleRel, Roles, ElasticUser
from . lib import ElasticSearch

elastic = ElasticSearch.ElasticSearch(host=app.config['ELASTIC_HOST'], port=app.config['ELASTIC_PORT'])

def getRolesList():
    query = db_es.session.query(Roles)
    result = []
    try:
        result = query.filter(Roles.id != 0).order_by(Roles.id).all()
    except exc.OperationalError as e:
        print("getRolesList: sql error: ", str(e))
    except Exception as e:
        print("getRolesList: unexpected sql error: ", str(e))

    return result

def getUsersByCompanyID(_id):
    query = db_es.session.query(UserCompanyRel)
    try:
        usr_list = query.filter(UserCompanyRel.company_id == _id).all()
    except exc.OperationalError as e:
        print("getUsersByCompanyID: sql error: ", str(e))
        return []
    except Exception as e:
        print("getUsersByCompanyID: unexpected sql error: ", str(e))
        return []

    users_list = []

    for usr in usr_list:
        # print("------------>>> user_id = ", usr.user_id)
        user_rec = elastic.getUser(usr.user_id)
        users_list.append(user_rec)

    return users_list

def getCompanyByUserID(_id):
    query = db_es.session.query(UserCompanyRel)
    try:
        comp_info = query.filter(UserCompanyRel.user_id == _id).first()
    except exc.OperationalError as e:
        print("getCompanyByUserID: sql error: ", str(e))
        return []
    except Exception as e:
        print("getCompanyByUserID: unexpected sql error: ", str(e))
        return []

    comp_rec = elastic.getCompany(comp_info.company_id)

    return comp_rec

def saveUser2DB(_new_user_id, _role_id, _company_id, _plain_passwd):
    """ Сохранение отношений user - role, user - company в БД """
    try:
        new_user_company_rel = UserCompanyRel(user_id=_new_user_id, company_id=_company_id)
        db_es.session.add(new_user_company_rel)
        new_user_role_rel = UserRoleRel(user_id=_new_user_id, role_id=_role_id)
        db_es.session.add(new_user_role_rel)
        db_es.session.commit()

        new_user_pass = ElasticUser(_id=_new_user_id, password=_plain_passwd)
        db.session.add(new_user_pass)
        db.session.commit()

    except exc.SQLAlchemyError as e:
        db_es.session.rollback()
        print("saveUser2DB: DB error: " + str(e))

@app.route('/')
def main_index():

    form = LoginForm(request.form)

    return render_template(
        'index.html',
        form=form,
    )

@app.route('/user_detail/<string:_id>')
@login_required
def user_detail_index(_id):
    """ Получаем и готовим к показу (в модальном окне) пользователя по ID  """

    form = LoginForm(request.form)

    user_rec = elastic.getUser(_id)
    query = db.session.query(ElasticUser)
    plain_password = ''

    company_rec = getCompanyByUserID(_id)
    print("user_detail_index: company_rec = ", company_rec)
    company_name = ''
    try:
        company_name = company_rec['source']['name']
    except:
        pass

    try:
        result = query.filter(ElasticUser._id == _id).first()
        plain_password = result.password
    except exc.OperationalError as e:
        print("user_detail_index: sql error: ", str(e))
    except Exception as e:
        print("user_detail_index: unexpected sql error: ", str(e))

    user_data = {
        'id': user_rec['id'],
        'name': user_rec['source']['fullname'],
        'email': user_rec['source']['email'],
        'login': user_rec['source']['login'],
        'password': plain_password,
        'company_name': company_name,
    }

    return render_template(
        'user_details.html',
        user=user_data,
        form=form,
    )

@app.route('/company_users/<string:_id>')
@login_required
def company_users_index(_id):
    """ Получаем и готовим к показу список пользователей по ID компании """
    form = LoginForm(request.form)

    users_list = []
    users_list = getUsersByCompanyID(_id)

    roles_list = getRolesList()

    return render_template(
        'company_users.html',
        users_list=users_list,
        roles_list=roles_list,
        form=form,
        page_size=20,
        company_id=_id,
    )

@app.route('/users')
@login_required
def users_index():

    form = LoginForm(request.form)

    users_list = elastic.getUsers()
    companies_list = elastic.getCompanies()
    roles_list = getRolesList()

    return render_template(
        'users.html',
        users_list=users_list,
        companies_list=companies_list,
        roles_list=roles_list,
        form=form,
        page_size=20,
    )

@app.route('/companies')
@login_required
def companies_index():

    form = LoginForm(request.form)

    companies_list = elastic.getCompanies()

    return render_template(
        'companies.html',
        companies_list=companies_list,
        form=form,
        page_size=20,
    )

@app.route('/check_login_exists', methods=['POST'])
def check_login_exists():

    login_name = request.form['login_name']

    status = elastic.checkLoginExists(login_name)

    return json.dumps({'status': status, })

@app.route('/add_company', methods=['POST'])
def add_company():

    name = request.form['name']
    city = request.form['city']
    email = request.form['email']
    phone = request.form['phone']
    description = request.form['description']

    elastic.addCompany(name=name, city=city, email=email, phone=phone, description=description)

    return json.dumps({'status': 'OK', })

@app.route('/add_user', methods=['POST'])
def add_user():

    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']
    login_name = request.form['login_name']
    description = request.form['description']
    company_id = request.form['company_id']
    role_id = request.form['role_id']
    position = request.form['position']
    description = request.form['description']
    avatar = request.form['avatar']
    passwd = request.form['passwd']

    if not login_name.isdigit():
        return json.dumps({'status': None, 'message': "Логин должен быть числовым (содержать только цифры).", })

    if elastic.checkLoginExists(login_name):
        return json.dumps({'status': None, 'message': "Пользователь с таким логином уже существует.", })

    plain_passwd = passwd
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()

    new_user_id = elastic.addUser(company_id=company_id, fullname=fullname, login=login_name, passwd=passwd,
                                  email=email, phone=phone, position=position, avatar=avatar, description=description)

    if new_user_id:
        saveUser2DB(new_user_id, role_id, company_id, plain_passwd)
        return json.dumps({'status': 'OK', })
    else:
        return json.dumps({'status': None, 'message': "Не удалось создать пользователя.", })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Вы уже вошли на сайт.")
        return redirect("/")

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            User.try_login(username, password)
        except ValueError:
            flash('Некорректный логин или пароль. Попробуйте повторно войти.', 'danger')
            # return render_template('index.html', form=form)
            return redirect("/")

        try:
            user = User.query.filter_by(username=username).first()
        except exc.OperationalError as e:
            print("login: sql error: ", str(e))
        except Exception as e:
            print("login: unexpected sql error: ", str(e))


        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash(u"Вы успешно вошли на сайт", "success")
        return redirect("/")

    if form.errors:
        flash(form.errors, 'danger')

    return render_template("index.html", form=form)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
