"""
PSQL Database Access
"""


import pandas as pd
import os
import psycopg2
from sqlalchemy import create_engine

class Db:
    def __init__(self, conn):
        self.conn = conn

    @staticmethod
    def init_db():
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        engine = create_engine(DATABASE_URL)
        conn_e = engine.connect()
        print("----------------")
        print(DATABASE_URL)
        return Db(conn)

    # sample function: need to modify format
    # insert_user: dictionary
    # need to check for valid class and school
    # return uid of user just added, returns -1 on failure
    def insert_user(self, bio):

        uid = -1
        user_bio = tuple(bio.values())
        user_str = "'" + "', '".join(user_bio) + "'"

        sql = 'insert into users (school_email, uni, first_name, mid_name, last_name, major, minor) values (%s)' % (user_str,)

        try:
            self.conn.cursor().execute(sql, (user_bio,))
            self.conn.commit()
            sql2 = 'select max(uid) as latest_user from users' 
            cur2 = self.conn.cursor()
            cur2.execute(sql2)
            uid = int(cur2.fetchone()[0])
            cur2.close()
        except Exception as e:
            print('failed to insert into users: ' + str(e))
            return -1

        return uid


    # insert_course individually
    # input dictionary
    # return cid of course just added, return -1 on failure
    # insert course information into course table
    def insert_course(self, info):
        cid = -1
        course_info = tuple(info.values())
        course_str = "'" + "', '".join(course_info) + "'"
        sql = "insert into courses (dept, code, sect, year_sem, description, link) values (%s)" %(course_str,)
        try:
            self.conn.cursor().execute(sql, (course_str,))
            self.conn.commit()
            sql2 = 'select max(cid) as latest_course from courses' 
            cur2 = self.conn.cursor()
            cur2.execute(sql2)
            cid = int(cur2.fetchone()[0])
            cur2.close()
        except Exception as e:
            print('failed to insert into course: ' + str(e))
            return -1
        return cid

    def insert_course_df(self, course_df):
        course_df.to_sql(name = 'course', con = conn_e, if_exists = 'append', index = False)