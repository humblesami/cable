import os
import sys
import json
import importlib
import traceback
from pathlib import Path

from psycopg2 import connect
from django.core.management import call_command
from django.core.management.base import BaseCommand
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Command(BaseCommand):
    help = 'setting up db i.e. create db or drop db for dev purpose'
    settings_dir = os.path.dirname(__file__)
    str = 'website/management/commands'
    base_directory = ''
    if str in settings_dir:
        base_directory = settings_dir.replace(str, '')
    else:
        str = 'website\\management\\commands'
        base_directory = settings_dir.replace(str, '')

    def connect_host(self, database_info, active_db):
        con = 'Unsupported db engine'
        if active_db == 'postgresql':
            con = connect(
                database='postgres',
                user=database_info['USER'],
                password=database_info['PASSWORD'],
            )
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return con

    def init_execution(self, hard_reset, create):
        database_info = {}
        res = 'Unknown'
        config_path = '{}config.json'
        config_path = config_path.format(self.base_directory)
        config_info = False

        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        try:
            with open(config_path, 'r') as config:
                config_info = json.load(config)
        except:
            db_path = Path.as_posix(BASE_DIR) + '/db.sqlite3'
            if os.path.exists(db_path):
                os.remove(db_path)
            return 'done'

        db_engine = None
        db_config = None
        if config_info:
            db_info = config_info.get('db_info')
            if db_info:
                db_config = db_info.get('config')
                db_engine = db_info.get('name')

        if db_engine == 'sqlite':
            db_path = Path.as_posix(BASE_DIR) + '/db.sqlite3'
            if os.path.exists(db_path):
                os.remove(db_path)
            return 'done'

        db_host_connection = 'Wrong connection Info'
        try:
            db_host_connection = self.connect_host(db_config, db_engine)
        except Exception as e:
            db_host_connection = str(e)
            return db_host_connection
        if type (db_host_connection) is str:
            return db_host_connection

        db_cursor = db_host_connection.cursor()
        if hard_reset:
            db_name = db_config['NAME']
            stmt = """
                        SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity
                        WHERE pg_stat_activity.datname='""" + db_name + """'
                        """
            db_cursor.execute(stmt)
            stmt = 'DROP DATABASE if exists ' + db_name
            db_cursor.execute(stmt)

            db_cursor.execute('DROP DATABASE if exists ' + db_name)
            db_cursor.execute('CREATE DATABASE ' + db_config['NAME'])
            res = 'done'
        elif create:
            db_cursor.execute('CREATE DATABASE ' + db_config['NAME'])
        db_cursor.close()
        db_host_connection.close()
        return res

    def add_arguments(self, parser):
        parser.add_argument('-hard', '--hard',
                            action='store_true',
                            help='drop database if exists and create new one')
        parser.add_argument('-c', '--create',
                            action='store_true',
                            help='create database if does not exists')

    def handle(self, *args, **kwargs):
        try:
            hard_reset = True
            create = True
            res = self.init_execution(hard_reset, create)
            if res == 'done':
                print('Database created')
                importlib.import_module('del')
                call_command('makemigrations')
                call_command('migrate')
                root_path = os.path.dirname(__file__)
                root_path = os.path.dirname(root_path)
                root_path = os.path.dirname(root_path)
                #Pinter@rt5
                call_command('loaddata', root_path + '/fixtures/data.json')
            else:
                print('Failed because ' + res)
        except:
            eg = traceback.format_exception(*sys.exc_info())
            error_message = ''
            cnt = 0
            for er in eg:
                cnt += 1
                if not 'lib/python' in er and not 'lib\site-packages' in er:
                    error_message += " " + er
            print('Error ' + error_message)
