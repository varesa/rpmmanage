from celery import Celery
from celery.signals import worker_init

import db

@worker_init.connect
def initialize_db_session():
    database = db.Db()
