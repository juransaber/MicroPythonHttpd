DataConfigPathName = "data.config";
HTMLPathName = "index.html";


def storeData():
    global PinData;
    global DataConfigPathName;
    data = "";
    for i in [0,0,0,0,0,0]:
        data += str(i);
    print("-----------1")
    try:
        f = open(DataConfigPathName, 'w')
        print("-----------2")
        f.write(data);
        print("-----------3")
    finally:
        print("-----------4")
        if 'f' in locals() and f:
            print("-----------5")
            f.close();

storeData()
