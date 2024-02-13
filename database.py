import sqlalchemy as sql
from sqlalchemy import inspect
import os.path

user_data = None
engine, connection, metadata = None, None, None

def init_db():
    global engine
    global connection
    global metadata
    global user_data

    if not os.path.isfile("users.db"):
        engine = sql.create_engine("sqlite:///users.db", echo=True)
        connection = engine.connect()
        metadata = sql.MetaData()

        inspector = inspect(engine)

        # Проверяем, существует ли уже таблица в базе данных
        if 'user_info' not in inspector.get_table_names():
            user_data = sql.Table('user_info', metadata,
                sql.Column('user_id', sql.Integer, primary_key=True),
                sql.Column('user_name', sql.Text),
                sql.Column('user_login', sql.Text),
                sql.Column('user_password', sql.Text),
                sql.Column('user_email', sql.Text)
            )
            metadata.create_all(engine)
        else:
            # Если таблица уже существует, получаем объект таблицы
            user_data = sql.Table('user_info', metadata, autoload_replace=True, autoload_with=engine)
    else:
        engine = sql.create_engine("sqlite:///users.db", echo=False)
        connection = engine.connect()
        metadata = sql.MetaData()
        user_data = sql.Table('user_info', metadata, autoload_replace=True, autoload_with=engine)

def register_user(name=None, login=None, password=None, email=None) -> str:
    temp = isValid(name, login, password, email)
    if temp[0]:
        query_data = user_data.insert().values([
            {'user_name':name, 'user_login':login, 'user_password':password, 'user_email':email}
        ])
        connection.execute(query_data)
        connection.commit()
    return temp[1]

def get_all_data() -> list: #list of tuples
    query = sql.select(user_data)
    return connection.execute(query).fetchall()

def login_user(login=None, password=None) -> tuple:
    temp = isRegistered(login, password)
    if temp:
        return (True, 'Успешно!')
    return (False, f"Логин/пароль неверны!")

def isRegistered(login, password):
    data = get_all_data()
    #check login
    for i in data:
        if login.lower()==i[2].lower() and password==i[4]:
            return True
            break
    return False

def isValid(name, login, password, email) -> tuple:
    data = get_all_data()
    #check login
    for i in data:
        if login.lower() == i[2].lower():
            return (False, f'Пользователь с логином {login} уже существует')
            break
        if email.lower() == i[3].lower():
            return (False, f'Пользователь с почтой {email} уже существует')
            break
    #check password
    if(len(password)<8):
        return (False, 'Пароль короче 8 символов')
    #check email
    if('@' not in email) or ('.com' not in email) and ('.ru' not in email):
        return (False, 'Проверьте правильность написания вашей почты')
    return (True, 'Успешно!')

def name_by_login(login):
    data = get_all_data()
    for user in data:
        if user[2].lower() == login.lower():
            name = user[2]
            return name
        
def email_by_login(login):
    data = get_all_data()
    for user in data:
        if user[2].lower() == login.lower():
            email = user[3]
            return email
        
def clear_db():
    if user_data is not None:
        delete_stmt = user_data.delete()
        connection.execute(delete_stmt)
        print("All records cleared from the table.")

def update_user(login, new_name=None, new_login=None, new_password=None, new_email=None):
    user_table = user_data

    query = sql.select([user_table]).where(user_table.c.user_login == login)

    result = connection.execute(query).fetchone()

    if result:
        user_id = result['user_id']
        update_data = {}
        if new_name is not None:
            update_data['user_name'] = new_name
        if new_login is not None:
            update_data['user_login'] = new_login
        if new_password is not None:
            update_data['user_password'] = new_password
        if new_email is not None:
            update_data['user_email'] = new_email
        update_query = user_table.update().where(user_table.c.user_id == user_id).values(**update_data)
        connection.execute(update_query)

        return True, "Данные пользователя успешно обновлены."
    else:
        return False, f"Пользователь с логином {login} не найден."


#0 - id
#1 - name
#2 - login
#3 - email
#4 - password