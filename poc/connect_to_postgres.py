import psycopg2
import config as appcfg


config = appcfg.AppConfig(r"C:\repos\github\AndreyQC\web-flask\poc\config.yaml")
print(config.pg_db_connection_string)

conn = psycopg2.connect(config.pg_db_connection_string)

q = conn.cursor()
q.execute("""select
    lng.id,
    json_build_object(
      'id', lng.id,
      'language_name', lng.language_name,
      'language_shortname', lng.language_shortname,
      'created_at', lng.created_at,
      'changed_at', lng.changed_at
    )
FROM words."language" as lng;""")

print(q.fetchone())

conn.close()