import network
from machine import Pin

from MicroPythonHttpd import MicroPythonHttpd

PinArray = []

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
    for p in [16,5,4,0,2]:
        pin = Pin(p, Pin.OUT,value=1);
        PinArray.append(pin);
    pass

def postOperate(params):
    print(params)
    switchNum = int(params["switchNum"]);
    pin = None;
    if switchNum >= 0 and switchNum < len(PinArray):
        pin = PinArray[switchNum]
        if int(params["isOn"]) == 0:
            pin.off();
        else:
            pin.on();
        return 0, "ok"; #code = 0, message = "ok"
    else:
        return -1, "switchNum is not support!"; #code = 0, message = "zzzz"


doConnect();
initPins();
try:
    f = open('index.html', 'r')
    html = f.read()
    #print(html)
    httpd = MicroPythonHttpd(html, 80)
    httpd.useGet("/postOperate", postOperate);
    httpd.usePost("/postOperate", postOperate);
    httpd.start() #block;
finally:
    if f:
        f.close()
