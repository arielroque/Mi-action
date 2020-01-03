import sys
from controller import MiBand3, BluetoothScanner
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse


class Authentication(Resource):
    def post(self, address):
        global miband

        miband = MiBand3(address, debug=True)
        miband.setSecurityLevel(level="medium")
        miband.initialize()
        response = miband.authenticate()
        return jsonify({"Authentication": str(response)})

    def delete(self):
        return jsonify({"Status": "fdf"})


class MibandSteps(Resource):
    def get(self):
        global miband
        print(miband)
        response = miband.get_steps()
        return jsonify(response)


class MibandBattery(Resource):
    def get(self):
        global miband
        battery = miband.get_battery_info()
        return jsonify({"Battery", battery})


class MibandHeartRate(Resource):
    def get(self):
        global miband, heartRate
        miband.start_raw_data_realtime(heart_measure_callback=handleHeartRate)

        return jsonify({"HeartRate": heartRate})


class BluetoothDevices(Resource):
    def get(self):
        bluetoothScanner = BluetoothScanner()
        return jsonify({"Devices": bluetoothScanner.discover()})


def handleHeartRate(rate):
    global heartRate
    heartRate = rate


miband = None
heartRate = None

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

api.add_resource(Authentication, '/auth', '/auth/<string:address>')
api.add_resource(BluetoothDevices, '/devices')
api.add_resource(MibandSteps, '/steps')
api.add_resource(MibandHeartRate, '/heart')
api.add_resource(MibandBattery, '/battery')


if(__name__ == '__main__'):
    app.run(debug=True)
