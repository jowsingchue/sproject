from bottle import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime
import json


Base = declarative_base()


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # def __repr__(self):
    #     return 'timestamp = %s\nlatitude = %f, longitude = %f' \
    #         % (self.timestamp, self.latitude, self.longitude)

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
    return "Hello World!!!!"


@app.post('/log')
def store():
    t = datetime.datetime.strptime(
        json.loads(request.POST.get('timestamp')), '%Y-%m-%dT%H:%M:%S.%f')
    flat = request.POST.get('latitude')
    flon = request.POST.get('longitude')

    # Insert a Person in the person table
    new_log = Log(timestamp=t, latitude=flat, longitude=flon)
    session.add(new_log)
    session.commit()

    return
    # return request.body


run(app, host='0.0.0.0', port=8080, debug=True, reloader=True)
