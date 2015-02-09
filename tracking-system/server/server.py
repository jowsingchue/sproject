from bottle import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
import datetime
import bson.json_util
import json


Base = declarative_base()


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    ax = Column(Integer, nullable=True)
    ay = Column(Integer, nullable=True)
    az = Column(Integer, nullable=True)
    gx = Column(Integer, nullable=True)
    gy = Column(Integer, nullable=True)
    gz = Column(Integer, nullable=True)

    # def __repr__(self):
    #     return 'timestamp = %s\nlatitude = %f, longitude = %f' \
    #         % (self.timestamp, self.latitude, self.longitude)


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    data = json.dumps(data) # this will fail on non-encodable values, like other classes
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
engine = create_engine('sqlite:///logs.db')

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


@app.get('/log')
def show():
    obj = session.query(Log).order_by(Log.id.desc()).first()
    result = json.dumps(obj, cls=AlchemyEncoder)
    return result


@app.post('/log')
def store():
    t = datetime.datetime.strptime(
        json.loads(request.POST.get('timestamp')), '%Y-%m-%dT%H:%M:%S')
    flat = request.POST.get('latitude')
    flon = request.POST.get('longitude')
    ax = request.POST.get('ax')
    ay = request.POST.get('ay')
    az = request.POST.get('az')
    gx = request.POST.get('gx')
    gy = request.POST.get('gy')
    gz = request.POST.get('gz')

    # Insert a Person in the person table
    new_log = Log(timestamp=t, latitude=flat, longitude=flon,
                  ax=ax, ay=ay, az=az, gx=gx, gy=gy, gz=gz)
    session.add(new_log)

    session.commit()

    # return
    # return request.body


run(app, host='0.0.0.0', port=8080, debug=True, reloader=True)
