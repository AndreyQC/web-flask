import ruamel.yaml as yaml
import json
import os


class Config(object):
    def __init__(self, yaml_config_file):
        with open(yaml_config_file) as stream:
            try:
                yaml_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        self.PG_DB_HOST = yaml_config['databases']['postgres']['host']
        self.PG_DB_PORT = yaml_config['databases']['postgres']['port']
        self.PG_DB_SSLMODE = yaml_config['databases']['postgres']['sslmode']
        self.PG_DB_DBNAME = yaml_config['databases']['postgres']['dbname']
        self.PG_DB_USER = yaml_config['databases']['postgres']['user']
        self.PG_DB_TARGET_SESSION_ATTRS = yaml_config['databases']['postgres']['target_session_attrs']
        self.PG_DB_PWD = os.environ[yaml_config['databases']['postgres']['password']] 
        self.PG_DB_CONNECTION_STRING = f"""
            host={self.PG_DB_HOST}
            port={self.PG_DB_PORT}
            sslmode={self.PG_DB_SSLMODE}
            dbname={self.PG_DB_DBNAME}
            user={self.PG_DB_USER}
            password={self.PG_DB_PWD}
            target_session_attrs={self.PG_DB_TARGET_SESSION_ATTRS}
            """

    @property
    def connection_string(self):
        return f"""
            host={self.PG_DB_HOST}
            port={self.PG_DB_PORT}
            sslmode={self.PG_DB_SSLMODE}
            dbname={self.PG_DB_DBNAME}
            user={self.PG_DB_USER}
            password={self.PG_DB_PWD}
            target_session_attrs={self.PG_DB_TARGET_SESSION_ATTRS}
            """


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    def __init__(self, yaml_config_file):
        super(DevConfig, self).__init__(yaml_config_file)    


# https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object

if __name__ == '__main__':


    config = DevConfig(r"C:\repos\github\AndreyQC\web-flask\poc\config.yaml")
    print(config.pg_db_connection_string)
    print(config.DEBUG)

# $env:AZURE_RESOURCE_GROUP = 'MyTestResourceGroup'
# https://www.tutorialspoint.com/how-to-set-environment-variables-using-powershell