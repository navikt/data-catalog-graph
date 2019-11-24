import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from psycopg2.extras import RealDictCursor
import logging

class Database:

    def __init__(self):
        env_path = Path('..') / '.env'
        load_dotenv(dotenv_path=env_path)
        dsn = os.getenv("DATABASE_URI") 
        self.dsn = dsn
        self.conn = None

    def open_connection(self):
        try:
            if(self.conn is None):
                self.conn = psycopg2.connect(self.dsn)
        except psycopg2.DatabaseError as e:
            logging.error(e)
        finally:
            logging.info('Connection opened successfully.')

    def fetchone(self, query):
        try:
            self.open_connection()
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                if any(x in query for x in ['select','SELECT']):
                    cur.execute(query)
                    result = cur.fetchone()
                    return result
        except psycopg2.DatabaseError as e:
            logging.error(e)
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')
  

    def execute(self, query):
        try:
            self.open_connection()
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                if any(x in query for x in ['select','SELECT']):
                    cur.execute(query)
                    result = cur.fetchall()
                    return result
                else:
                    result = cur.execute(query)
                    self.conn.commit()
                    affected = f"{cur.rowcount}"
                    cur.close()
                    return affected
        except psycopg2.DatabaseError as e:
            logging.error(e)
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')
  