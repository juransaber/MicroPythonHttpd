import time
import network
from machine import Pin

from MicroPythonHttpd import MicroPythonHttpd

PinArray = [16,5,4,0,2,14,12,13,15,3,1,10,9]

def doConnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('MZY', '20085151')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def initPins():
    for p in PinArray:
        pin = Pin(p, Pin.OUT,value=1);
    pass

def postOperate(params):
    print(params)
    if int(params["switchNum"]) >= 0 and int(params["switchNum"]) < len(PinArray):
        pass
    if int(params["isOn"]) == 0:
        pin.off();
    else:
        pin.on();

    return "{\"code\":0, \"message\":\"ok\"}"

doConnect();
initPins();
httpd = MicroPythonHttpd("sssssssss", 80)
httpd.useGet("/postOperate", postOperate);
httpd.usePost("/postOperate", postOperate);
httpd.start() #block;
