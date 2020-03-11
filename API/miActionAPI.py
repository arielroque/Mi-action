import sys
from service import *
from controller import MiBand3, BluetoothScanner
from persistence import *
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from constants import General

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

api.add_resource(Authentication, '/auth', '/auth/<string:address>')
api.add_resource(BluetoothDevices, '/devices')
api.add_resource(MibandSteps, '/steps')
api.add_resource(MibandHeartRate, '/heart')
api.add_resource(MibandBattery, '/battery')
api.add_resource(MibandStepsPersistence, '/stepsPersistence')
api.add_resource(MibandHeartPersistence, '/heartPersistence')
Persistence().prepare_database()

if(__name__ == '__main__'):
    app.run(debug=True)
