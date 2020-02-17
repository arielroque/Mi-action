import sys
import os
import sqlite3
from controller import MiBand3, BluetoothScanner
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from constants import General


class Authentication(Resource):
    def get(self):
        global miband

        if(is_device_connected()):
            return jsonify({"Status": "Connected"})

        return jsonify({"Status": "Disconnected"})

    def post(self, address):
        global miband

        miband = MiBand3(address, debug=True)
        miband.setSecurityLevel(level="medium")
        miband.initialize()
        response = miband.authenticate()
        return jsonify({"Authentication": str(response)})

    def delete(self):
        global miband

        if(is_device_connected()):
            miband.disconnect()


class MibandSteps(Resource):
    def get(self):
        global miband

        if(is_device_connected()):
            response = miband.get_steps()
            return jsonify({
                "Steps": response[0],
                "Meters": response[1]})
        else:
            return jsonify({
                "Steps": "DEVICE NOT CONNECT",
                "Meters": "DEVICE NOT CONNECT"})


class MibandBattery(Resource):
    def get(self):
        global miband

        """if(is_device_connected()):
            battery = miband.get_battery_info()
            return jsonify({battery})
        else:
            return jsonify({"Battery", "DEVICE NOT CONNECT"})"""
        miband.listening_button()


class MibandHeartRate(Resource):
    def get(self):
        global miband, heart_rate

        if(is_device_connected()):
            miband.start_raw_data_realtime(
                heart_measure_callback=handle_heart_rate)
            return jsonify({"HeartRate": heart_rate})

        return jsonify({"HeartRate": "DEVICE NOT CONNECT"})


class BluetoothDevices(Resource):
    def get(self):

        bluetoothScanner = BluetoothScanner()
        return jsonify({"Devices": bluetoothScanner.discover()})


def prepare_database():
    folders = os.listdir()

    if(General.DATABASE_NAME not in folders):
        conn = sqlite3.connect(General.DATABASE_NAME)
        c = conn.cursor()

        sql = """CREATE TABLE users(
		          id integer unique primary key autoincrement,
		           name text)
		      """
        c.executescript(sql)
        conn.commit()
        conn.close()


def is_device_connected():
    global miband
    if(miband == None):
        return False
    return miband.is_device_connected()


def handle_heart_rate(rate):
    global heart_rate
    heart_rate = rate


miband = None
heart_rate = None

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
