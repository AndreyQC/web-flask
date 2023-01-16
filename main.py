from flask import Flask
from config import DevConfig
import psycopg2
import datetime


class DBcontext():
    def __init__(self, app):
        self.connectionstring = app.config['PG_DB_CONNECTION_STRING']

    def run_query(self, query):
        conn = psycopg2.connect(self.connectionstring)

        q = conn.cursor()
        q.execute(query)

        res = q.fetchone()
        conn.close()
        return (res)


app = Flask(__name__)
app.config.from_object(
    DevConfig(r"C:\repos\github\AndreyQC\web-flask\poc\config.yaml"))
dbcontext = DBcontext(app)


class User_Factory():
    def __init__(self, dbcontext):
        self.res = dbcontext.run_query("""select
                            lng.id,
                            json_build_object(
                            'id', lng.id,
                            'language_name', lng.language_name,
                            'language_shortname', lng.language_shortname,
                            'created_at', lng.created_at,
                            'changed_at', lng.changed_at
                            )
                        FROM words."language" as lng;"""
                                       )

    class User():
        def __init__(self, id, user_dict):
            self.user_name = user_dict.get('user_name', 'unknown')
            self.user_id = user_dict.get('id', 0)
            self.changed_at = user_dict.get('changed_at', datetime.now())
            self.updated_at = user_dict.get('updated_at', datetime.now())
            if self.user_id == 0:
                self.saved_in_database = False

        def __repr__(self):
            return f"<User '{self.user_name}'>"


@app.route('/')
def home():
    return '<h1>Hello World! {{ app.config["PG_DB_CONNECTION_STRING"] }} </h1>'


if __name__ == '__main__':
    users = User_Factory(dbcontext)
    user = users.User(id=0, username="fdf")

    # print(app.config)
    # print(app.config['PG_DB_CONNECTION_STRING'])
    # print(db.connectionstring)
    # res = db.run_query("""select
    #         lng.id,
    #         json_build_object(
    #         'id', lng.id,
    #         'language_name', lng.language_name,
    #         'language_shortname', lng.language_shortname,
    #         'created_at', lng.created_at,
    #         'changed_at', lng.changed_at
    #         )
    #     FROM words."language" as lng;"""
    #                    )
    # print(res)
    # app.run()
