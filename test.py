i = 0
def resetPins():
    global i
    i = i+1;
    print(i)
    if i == 10:
        i = 0;
        c = 111 / i;
try:
    for p in range(0, 30):
        resetPins()
except Exception as e:
    print(e)

print(111111, i)
