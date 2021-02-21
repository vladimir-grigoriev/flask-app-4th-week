class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False