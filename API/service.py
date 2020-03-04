import sys
import os
from persistence import *
from controller import MiBand3, BluetoothScanner
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse


class Authentication(Resource):
    def get(self):
        global miband

        if(is_device_connected()):
            return jsonify({"Status": "Connected"})

        return jsonify({"Status": "Disconnected"})

    def post(self, address):
        global miband

        os.system("sudo systemctl restart bluetooth.service")
        miband = MiBand3(address, debug=True)
        miband.setSecurityLevel(level="medium")
        miband.initialize()
        response = miband.authenticate()

        return jsonify({"Authentication": str(response)})

    def delete(self):
        global miband

        miband.disconnect()
        os.system("sudo systemctl restart bluetooth.service")


class MibandHeartPersistence(Resource):
    def get(self):
        response = Persistence().get_heart_data()
        return jsonify({
            "date": response[0],
            "heart": response[1]})


class MibandStepsPersistence(Resource):
    def get(self):
        response = Persistence().get_steps_data()
        return jsonify({
            "date": response[0],
            "steps": response[1]})


class MibandSteps(Resource):
    def get(self):
        global miband

        if(is_device_connected()):
            response = miband.get_steps()
            Persistence().insert_steps(response[0])
            return jsonify({
                "Steps": response[0],
                "Meters": response[1]})

        else:
            return jsonify({
                "Steps": "0",
                "Meters": "0"})


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
            Persistence().insert_heart_rate(heart_rate)
            return jsonify({"HeartRate": heart_rate})

        return jsonify({"HeartRate": "0"})


class BluetoothDevices(Resource):
    def get(self):

        bluetoothScanner = BluetoothScanner()
        return jsonify({"Devices": bluetoothScanner.discover()})


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
