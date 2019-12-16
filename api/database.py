import os
from urllib3.util import parse_url
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from psycopg2.extras import RealDictCursor
from flask import abort
import logging

from dataverk_vault import api as vault_api


class Database:

    def __init__(self):
        env_path = Path('..') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=True)
        try:
            dsn = os.environ["POSTGRES_DB"]
            postgres_role = os.environ["POSTGRES_ROLE"]
        except KeyError:
            secrets = vault_api.read_secrets()
            dsn = secrets["POSTGRES_DB"]
            postgres_role = os.environ["POSTGRES_ROLE"]
            self.vault_secret_path = os.environ["POSTGRES_VAULT_PATH"]
        self.dsn = dsn
        self.postgres_role = postgres_role
        self.conn = None

    def open_connection(self):
        try:
            self.conn = psycopg2.connect(self.dsn)
        except psycopg2.OperationalError:
            self._update_credentials()
            self.conn = psycopg2.connect(self.dsn)
            logging.warning(f"Fetching new postgres credentials")
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
                if query.startswith(('select', 'SELECT')):
                    cur.execute(query)
                    result = cur.fetchall()
                    return result
                else:
                    cur.execute(f"SET ROLE '{self.postgres_role}'")
                    result = cur.execute(query)
                    affected = f"{cur.rowcount}"
                    self.conn.commit()
                    cur.close()
                    return affected
        except psycopg2.DatabaseError as e:
            logging.error(e)
            abort(400, f"Error Message: {e}")
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    def _update_credentials(self):
        credentials = vault_api.get_database_creds(self.vault_secret_path)
        parsed_conn_string = parse_url(self.dsn)
        self.dsn = str(parsed_conn_string).replace(parsed_conn_string.auth, credentials)
