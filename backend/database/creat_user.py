# -*- coding: UTF-8 -*-
'''
@Project ：SE4GEO 
@File    ：creat_user.py
@IDE     ：PyCharm 
@Author  ：JUNJIE MU
@Date    ：2024/6/23 下午4:22 
@explain : 
'''

def creat_user():
    import psycopg2
    import os
    from dotenv import load_dotenv
    load_dotenv()
    db_name = os.getenv('DB_NAME')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    if not all([db_name, user, password, host]):
        raise ValueError("Plz set environment variables in .env file")
    try:
        conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host)
        cursor = conn.cursor()
        #Creat table
        creat_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            user_password VARCHAR(255) NOT NULL
        );
        """
        cursor.execute(creat_query)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as error:
        return error
