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
    return (False, f"Логин/пароль неверны! {get_all_data()}")

def isRegistered(login, password):
    data = get_all_data()
    #check login
    for i in data:
        if login==i[2] and password==i[4]:
            return True
            break
    return False

def isValid(name, login, password, email) -> tuple:
    data = get_all_data()
    #check login
    for i in data:
        if login == i[2]: #i[1] == login
            return (False, f'Пользователь с логином {login} уже существует')
            break
        if email == i[4]:
            return (False, f'Пользователь с почтой {email} уже существует')
            break
    #check password
    if(len(password)<8):
        return (False, 'Пароль короче 8 символов')
    #check email
    if('@' not in email) or ('.com' not in email) and ('.ru' not in email):
        return (False, 'Проверьте правильность написания вашей почты')
    return (True, 'Успешно!')
