#!/usr/bin/python

import os
import json
import ast
import random

from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

#import bson.json_util


###############################################################################
#
#   Database
#
Base = declarative_base()

class Log(Base):
	__tablename__ = 'logs'

	id = Column(Integer, primary_key=True)
	device_id = Column(Integer)
	timestamp = Column(DateTime, nullable=True)
	latitude = Column(Float, nullable=True)
	longitude = Column(Float, nullable=True)

	imu = relationship('Imu')

	# def __repr__(self):
	#     return 'timestamp = %s\nlatitude = %f, longitude = %f' \
	#         % (self.timestamp, self.latitude, self.longitude)


class Imu(Base):
	__tablename__ = 'imu'

	id = Column(Integer, primary_key=True)
	log_id = Column(Integer, ForeignKey('logs.id'))
	ax = Column(Integer, nullable=True)
	ay = Column(Integer, nullable=True)
	az = Column(Integer, nullable=True)
	gx = Column(Integer, nullable=True)
	gy = Column(Integer, nullable=True)
	gz = Column(Integer, nullable=True)
	dt = Column(Float, nullable=True)

	def __repr__(self):
		return '%d %d %d %d %d %d' % (self.ax, self.ay, self.az, self.gx, self.gy, self.gz)


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
					fields[field] = None
			# a json-encodable dict
			return fields

		return json.JSONEncoder.default(self, obj)

# Create an engine that stores data in the local directory's
engine = create_engine('sqlite:///database/logs.db')

# Create all tables in the engine. This is equivalent to 'Create Table'
# statements in raw SQL.
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a 'staging zone' for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


###############################################################################
#
#   Server
#

app = Flask(__name__)

@app.route( '/log', methods = [ 'POST' ] )
def store():
	post_data = request.json
	new_log = Log(
		device_id=post_data[0],
		timestamp=datetime.datetime.strptime(post_data[1],
											 '%Y-%m-%dT%H:%M:%S'),
		latitude=post_data[2],
		longitude=post_data[3])
	new_log.imu = []
	for e in post_data[4]:
		new_log.imu.append(Imu(
			ax=e[0], ay=e[1], az=e[2], gx=e[3], gy=e[4], gz=e[5], dt=e[6]
		))
	session.add(new_log)
	session.commit()

@app.route( '/log', methods = [ 'GET' ] )
def getLog():
	obj = session.query(Imu).order_by(Imu.id.desc()).limit(100).all()
	resultDictListStr = json.dumps(obj, cls=AlchemyEncoder)
	resultDictList = ast.literal_eval( resultDictListStr )
	return resultDictListStr

@app.route('/test1', methods = [ 'GET' ] )
def test1():
	obj = session.query(Imu).order_by(Imu.id.desc()).limit(10).all()

	resultDictListStr = json.dumps(obj, cls=AlchemyEncoder)

	resultDictList = ast.literal_eval( resultDictListStr )


	data = list()
	for i in range(80):
		data.append(i * 0.01)
	return render_template( 'test1.html', data=data )

@app.route( '/api/position', methods = [ 'GET' ] )
def position():
	obj = session.query(Log.latitude, Log.longitude).order_by(Log.id.desc()).first()
	resultDictListStr = json.dumps(obj, cls=AlchemyEncoder)
	resultDictList = ast.literal_eval( resultDictListStr )

	# latitude = resultDictList[0]
	# longitude = resultDictList[1]
	latitude = random.uniform(13.8475145, 13.8475145 + 0.001)
	longitude = random.uniform(100.5674436, 100.5674436 + 0.001)

	print latitude
	print longitude

	outputDict = {
		'lat': latitude,
		'lon': longitude
	}

	# return '{} {}'.format( latitude, longitude )
	return jsonify(**outputDict)


@app.route( '/', methods = [ 'GET' ] )
def index():
	obj = session.query(Log.latitude, Log.longitude).order_by(Log.id.desc()).first()
	resultDictListStr = json.dumps(obj, cls=AlchemyEncoder)
	resultDictList = ast.literal_eval( resultDictListStr )
	print resultDictList

	# latitude = resultDictList[0]
	# longitude = resultDictList[1]
	latitude = random.uniform(13.8475145, 13.8475145 + 0.001)
	longitude = random.uniform(100.5674436, 100.5674436 + 0.001)

	return render_template( 'index.html', latitude=latitude, longitude=longitude )

if __name__ == '__main__':
	#app.run( host='0.0.0.0', port=8080 )
	app.run( host='0.0.0.0', port=8080, debug=True )
	# app.run( debug=True )
