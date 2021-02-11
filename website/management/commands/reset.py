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
            con = con = connect(
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

        active_db = False
        db_engine=None
        if config_info:
            active_db = config_info.get('active_db')
            if active_db:
                db_config = config_info.get(active_db)
                if db_config:
                    database_info = config_info[active_db]
                    db_engine = database_info['ENGINE']


        if not db_engine == 'sqlite':
            db_path = Path.as_posix(BASE_DIR) + '/db.sqlite3'
            if os.path.exists(db_path):
                os.remove(db_path)
            return 'done'

        db_host_connection = 'Wrong connection Info'
        try:
            db_host_connection = self.connect_host(database_info, active_db)
        except Exception as e:
            db_host_connection = str(e)
            return db_host_connection
        if type (db_host_connection) is str:
            return db_host_connection

        db_cursor = db_host_connection.cursor()
        if hard_reset:
            db_cursor.execute('DROP DATABASE if exists ' + database_info['NAME'])
            db_cursor.execute('CREATE DATABASE ' + database_info['NAME'])
            res = 'done'
        elif create:
            db_cursor.execute('CREATE DATABASE ' + database_info['NAME'])
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
