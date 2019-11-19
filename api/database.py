from environs import Env
import psycopg2

def getConnection():

    env = Env()
    env.read_env()

    dsn = env.str('CONNECTION_DSN')
    conn = psycopg2.connect(dsn)

    return conn