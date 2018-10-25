import network
from machine import Pin

from MicroPythonHttpd import MicroPythonHttpd

DataConfigPathName = "data.config";
HTMLPathName = "index.html";

PinArray = []
PinNumArr = [0, 2, 16, 5, 4]
PinData = []
def doConnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.ifconfig (('192.168.1.20', '255.255.255.0', '223.5.5.5', '8.8.8.8'))
        wlan.connect('MZY', '20085151')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def initPins():
    global PinData;
    global DataConfigPathName;
    try:
        f = open(DataConfigPathName, 'r')
        data = f.read();
        PinData = [int(i) for i in data];
    except:
        PinData = [0] * len(PinNumArr);
    finally:
        if 'f' in locals() and f:
            f.close()

    for i in range(0, len(PinNumArr)):
        pNum = PinNumArr[i];
        pValue = PinData[i];

        pin = Pin(pNum, Pin.OUT, value=pValue);
        PinArray.append(pin);


def storeData():
    global PinData;
    global DataConfigPathName;
    data = "";
    for i in PinData:
        data += str(i);

    try:
        f = open(DataConfigPathName, 'w')
        f.write(data);
    finally:
        if 'f' in locals() and f:
            f.close();

def postOperate(params):
    print(params)
    switchNum = int(params["switchNum"]);
    pin = None;

    if switchNum >= 0 and switchNum < len(PinArray):
        pin = PinArray[switchNum]
        PinData[switchNum] = int(params["isOn"]);
        print(PinData[switchNum]);
        if PinData[switchNum] == 0:
            pin.off();
        else:
            pin.on();

        storeData();

        return 0, PinData, "ok"; #code = 0, message = "ok"
    else:
        return -1, PinData, "switchNum is not support!"; #code = 0, message = "zzzz"


doConnect();
initPins();


try:
    f = open(HTMLPathName, 'r')
    html = f.read()
    #print(html)
    httpd = MicroPythonHttpd(html, 80)
    httpd.useGet("/postOperate", postOperate);
    httpd.usePost("/postOperate", postOperate);
    httpd.start() #block;
finally:
    if 'f' in locals() and f:
        f.close()
