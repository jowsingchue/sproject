from bottle import *
from sqlalchemy import create_engine, Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import bson.json_util
import json
import datetime

Base = declarative_base()


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    imu = relationship("Imu")

    # def __repr__(self):
    #     return 'timestamp = %s\nlatitude = %f, longitude = %f' \
    #         % (self.timestamp, self.latitude, self.longitude)


class Imu(Base):
    __tablename__ = 'imu'

    id = Column(Integer, primary_key=True)
    ax = Column(Integer, nullable=True)
    ay = Column(Integer, nullable=True)
    az = Column(Integer, nullable=True)
    gx = Column(Integer, nullable=True)
    gy = Column(Integer, nullable=True)
    gz = Column(Integer, nullable=True)
    log_id = Column(Integer, ForeignKey('logs.id'))

    def __repr__(self):
        return "%d %d %d %d %d %d" % (self.ax, self.ay, self.az, self.gx, self.gy, self.gz)


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other
                    # classes
                    data = json.dumps(data)
                    fields[field] = data
                except TypeError:
                    try:
                        data = json.dumps(data, default=bson.json_util.default)
                        fields[field] = data
                    except:
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

# Create an engine that stores data in the local directory's
engine = create_engine('sqlite:///log/logs.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


app = Bottle()


@app.get('/hello')
def hello():
    return "<h1>Hello World!</h1>"


@app.get('/log')
def show():
    obj = session.query(Log).order_by(Log.id.desc()).first()
    result = json.dumps(obj, cls=AlchemyEncoder)
    return result


@app.post('/log')
def store():
    post_data = request.json
    new_log = Log(
        timestamp=datetime.datetime.strptime(post_data[0],
                                             '%Y-%m-%dT%H:%M:%S'),
        latitude=post_data[1],
        longitude=post_data[2])
    new_log.imu = []
    for e in post_data[3:]:
        new_log.imu.append(Imu(
            ax=e[0], ay=e[1], az=e[2], gx=e[3], gy=e[4], gz=e[5]))
    session.add(new_log)
    session.commit()


run(app, host='0.0.0.0', port=8080, debug=True, reloader=True)
