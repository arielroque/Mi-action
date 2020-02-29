import sys
import os
import sqlite3
import collections
from datetime import datetime
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


class MibandHeartPersistence(Resource):
    def get(self):
        response = get_heart_data()
        return jsonify({
            "date": response[0],
            "heart": response[1]})


class MibandStepsPersistence(Resource):
    def get(self):
        response = get_steps_data()
        return jsonify({
            "date": response[0],
            "steps": response[1]})


class MibandSteps(Resource):
    def get(self):
        global miband

        if(is_device_connected()):
            response = miband.get_steps()
            insert_steps(response[0])
            return jsonify({
                "Steps": response[0],
                "Meters": response[1]})

        else:
            return jsonify({
                "Steps": "Device not connect",
                "Meters": "Device not connect"})


class MibandBattery(Resource):
    def get(self):
        global miband

        """if(is_device_connected()):
            battery = miband.get_battery_info()
            return jsonify({battery})
        else:
            return jsonify({"Battery", "Device not connect"})"""
        miband.listening_button()


class MibandHeartRate(Resource):
    def get(self):
        global miband, heart_rate

        if(is_device_connected()):
            miband.start_raw_data_realtime(
                heart_measure_callback=handle_heart_rate)
            insert_heart_rate(heart_rate)
            return jsonify({"HeartRate": heart_rate})

        return jsonify({"HeartRate": "Device not connect"})


class BluetoothDevices(Resource):
    def get(self):

        bluetoothScanner = BluetoothScanner()
        return jsonify({"Devices": bluetoothScanner.discover()})


def get_heart_data():
    conn = sqlite3.connect("data/"+General.DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM heart;
    """)

    heart_data = collections.OrderedDict()

    for line in cursor.fetchall():
        if(line[2] not in heart_data.keys()):
            l = []
            l.append(line[1])
            heart_data[line[2]] = l
        else:
            heart_data[line[2]].append(line[1])

    keys = list(heart_data.keys())
    keys.reverse()

    values = list(heart_data.values())
    values.reverse()

    response = []
    hearts = []
    dates = []

    for i in range(len(values)):
        if(i > 9):
            break
        average = sum(values[i])/len(values[i])
        hearts.append(average)
        dates.append(keys[i])
    conn.close()

    response.append(dates)
    response.append(hearts)

    return response


def get_steps_data():

    conn = sqlite3.connect("data/"+General.DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM steps;
    """)

    stepData = collections.OrderedDict()

    for line in cursor.fetchall():
        print(line)
        if(line[2] not in stepData.keys()):
            l = []
            l.append(line[1])
            stepData[line[2]] = l
        else:
            stepData[line[2]].append(line[1])

    keys = list(stepData.keys())
    keys.reverse()

    values = list(stepData.values())
    values.reverse()

    response = []
    steps = []
    dates = []

    for i in range(len(values)):
        if(i > 9):
            break
        average = sum(values[i])/len(values[i])
        steps.append(average)
        dates.append(keys[i])

    conn.close()

    response.append(dates)
    response.append(steps)

    return response


def insert_heart_rate(heart_rate):

    date = datetime.today().strftime('%d/%m')

    conn = sqlite3.connect("data/"+General.DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO heart(qtd, heartDate)
    VALUES (%d,'%s')
    """ % (heart_rate, date))

    conn.commit()
    conn.close()


def insert_steps(steps):
    date = datetime.today().strftime('%d/%m')

    conn = sqlite3.connect("data/"+General.DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO steps (qtd, stepDate)
    VALUES (%d,'%s')
    """ % (steps, date))

    conn.commit()
    conn.close()


def prepare_database():
    folders = os.listdir("data")
    print(folders)

    if(General.DATABASE_NAME not in folders):
        conn = sqlite3.connect("data/"+General.DATABASE_NAME)
        c = conn.cursor()

        sql = """CREATE TABLE steps(
		          id INTEGER unique PRIMARY KEY AUTOINCREMENT,
		           qtd INT NOT NULL,
                   stepDate DATE
                   )
		      """
        c.executescript(sql)
        conn.commit()

        sql2 = """CREATE TABLE heart(
		          id INTEGER unique PRIMARY KEY AUTOINCREMENT,
		           qtd INT NOT NULL,
                   heartDate DATE
                   )
		      """
        c.executescript(sql2)
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
api.add_resource(MibandStepsPersistence, '/stepsPersistence')
api.add_resource(MibandHeartPersistence, '/heartPersistence')

prepare_database()

if(__name__ == '__main__'):
    app.run(debug=True)
