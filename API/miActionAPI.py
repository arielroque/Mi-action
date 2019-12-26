import sys
from controller import MiBand3

def get_miband_info():
    print("INFO")

def get_heart_beat():
    print("HEART")

def get_steps():
    print("STEPS")

def send_message(message):
    print(message)

def send_alert():
    print("ALERTING")

def get_battery_info():
    print("Battery")

def authenticate_miband():
    print("AUTHENTICATE")


band = MiBand3("D8:1E:78:B2:11:46",debug=True)
band.setSecurityLevel(level = "medium")
band.initialize()
band.authenticate()