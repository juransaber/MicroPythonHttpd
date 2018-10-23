import network
from machine import Timer
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
    for p in [5,4,14,12]:
        pin = Pin(p, Pin.OUT,value=0);
        PinArray.append(pin);
    pass

hightLevelPins = [];
def postOperate(params):
    print(params)
    switchNum = int(params["switchNum"]);
    pin = None;
    if switchNum >= 0 and switchNum < len(PinArray):
        global hightLevelPins
        global i
        i = 0
        pin = PinArray[switchNum]
        pin.on();
        hightLevelPins.append(pin);
        return 0, "ok"; #code = 0, message = "ok"
    else:
        return -1, "switchNum is not support!"; #code = 0, message = "zzzz"

i = 0
def resetPins(t):
    global i
    i = i+1;
    if i == 10 and len(hightLevelPins) > 0:
        i = 0;
        for pin in hightLevelPins:
            pin.off();
        del hightLevelPins[:];

tim = Timer(-1)
tim.init(period=50, mode=Timer.PERIODIC, callback=resetPins)

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
