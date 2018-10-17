try:
    f = open('index.html', 'r')
    print(f.read())
finally:
    if f:
        f.close()
