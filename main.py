from flask import Flask
from config import DevConfig
import psycopg2
from psycopg2.extras import Json as pgJson
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
        self.db = dbcontext
        self.db_function_create = "api.fun_user_create"
        self.db_function_update = "api.fun_user_update"
        self.db_function_get_list = "api.fun_user_get_list"
        self.db_function_delete = "not implemented"
        self.db_function_get_by_id = "api.fun_user_get_by_id"

    def get_by_id(self, user_id):
        u = self.User({})
        res = dict()
        try:
            conn = psycopg2.connect(self.db.connectionstring)
            q = conn.cursor()
            
            p_json_user = pgJson({"id":user_id})
            p_json_current_user= pgJson({})
            p_json_current_session = pgJson({})

            q.execute(f"select * from  {self.db_function_get_by_id} ({p_json_user},{p_json_current_user},{p_json_current_session} );")
            result = q.fetchall()

            for row in result:
                res = row[0]
            

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)            


        finally:
            
            # closing database connection.
            if conn:
                q.close()
                conn.close()
                print("PostgreSQL connection is closed")
            # _jobdef = {'id': 1, 'name': 'product', 'amount': 230}
            # cur.execute("SELECT mrp_sp_insert_jobdef( %s )", (Json(_jobdef),) )    
            # 
        u.user_id = res.get('id', 0)
        u.user_name = res.get('user_name', 'unknown'),
        u.changed_at = res.get('changed_at', datetime.datetime.now())
        u.updated_at = res.get('updated_at', datetime.datetime.now())
        u.saved_in_database = res.get('saved_in_database', False) 
        return (u)   

    class User():
        def __init__(self, user_dict):
            if user_dict:
                self.user_name = user_dict.get('user_name', 'unknown')
                self.user_id = user_dict.get('id', 0)
                self.changed_at = user_dict.get('changed_at', datetime.now())
                self.updated_at = user_dict.get('updated_at', datetime.now())
                if self.user_id == 0:
                    self.saved_in_database = False
                else:
                    self.saved_in_database = True

        def __repr__(self):
            return f"<User '{self.user_name}'>"


@app.route('/')
def home():
    return '<h1>Hello World! {{ app.config["PG_DB_CONNECTION_STRING"] }} </h1>'


if __name__ == '__main__':
    users = User_Factory(dbcontext)
    user = users.get_by_id(82)
    print(user)
    # user = users.User(id=0, user_name="fdf")

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
