import sys
from controller import MiBand3, BluetoothScanner
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse


class Authentication(Resource):

    def __init__(self):
        self.band = None

    def post(self, address):
        self.band = MiBand3(address, debug=True)
        self.band.setSecurityLevel(level="medium")
        self.band.initialize()
        response = self.band.authenticate()
        return jsonify({"Authentication": str(response)})

    def delete(self):
        self.band.disableConnection()
        return jsonify({"Status": "fdf"})


class BluetoothDevices(Resource):
    def get(self):
        bluetoothScanner = BluetoothScanner()
        return jsonify({"Devices": bluetoothScanner.discover()})


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

api.add_resource(Authentication, '/auth', '/auth/<string:address>')
api.add_resource(BluetoothDevices, '/devices')


if(__name__ == '__main__'):
    app.run(debug=True)
