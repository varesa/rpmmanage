from flask import Flask
from flask.ext.celery import Celery

import db
import dbModels

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = "amqp://localhost"
app.config['CELERY_RESULT_BACKEND'] = "amqp://localhost"

celery = Celery(app)

database = db.Db()

if __name__ == '__main__':
    dbModels.create_tables(database.get_engine())

    session = database.get_session()
    session.add(dbModels.Test(id=1, name="abc"))
    session.commit()
    print(session.query(dbModels.Test).all())

    app.debug = True
    app.run(host="0.0.0.0")
