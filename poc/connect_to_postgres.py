import psycopg2

conn = psycopg2.connect("""
    host=rc1a-lsohunqdlnlwpe3j.mdb.yandexcloud.net
    port=6432
    sslmode=verify-full
    dbname=object-universe
    user=andreyqc
    password=<пароль пользователя>
    target_session_attrs=read-write
""")

q = conn.cursor()
q.execute('SELECT version()')

print(q.fetchone())

conn.close()