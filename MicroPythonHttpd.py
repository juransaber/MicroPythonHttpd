try:
    import usocket as socket
except:
    import socket

class MicroPythonHttpd:
    sock = None;
    port = 80;
    postMap = {};
    getMap = {};

    def __init__(self, html, port):
        self.servSock = socket.socket()
        self.html = html;
        # Binding to all interfaces - server will be accessible to other hosts!
        ai = socket.getaddrinfo("0.0.0.0", self.port)
        self.addr = ai[0][-1]

        self.servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def usePost(self, requestUri, handler):
        self.postMap[requestUri] = handler

    def useGet(self, requestUri, handler):
        self.getMap[requestUri] = handler

    def start(self):
        self.servSock.bind(self.addr)
        self.servSock.listen(self.port)
        while True:
            try:
                client, addr = self.servSock.accept()
                method, requestUri, paramsMap = self.parseRequest(addr, client.recv(4096).decode('utf-8'))
                print(requestUri)
                if method == "GET":
                    if requestUri == "/":
                        client.send("HTTP/1.1 200 OK\r\n\r\n")
                        client.send(self.html)
                    else:
                        code = -1;
                        message = ""
                        if requestUri in self.getMap:
                            handler = self.getMap[requestUri];
                            if callable(handler):
                                try:
                                    code, message = handler(paramsMap)
                                except:
                                    message = "handler error"
                            else:
                                message = "request uri not callable"
                        else:
                            message = "request uri not exist"

                        client.send("HTTP/1.1 200 OK\r\n\r\n")
                        client.send("{\"code\":"+str(code)+",\"message\":\"" + message + "\"}")

                elif method == "POST":
                    code = -1;
                    message = ""
                    if requestUri in self.postMap:
                        handler = self.postMap[requestUri];

                        if callable(handler):
                            try:
                                code, message = handler(paramsMap)
                            except:
                                message = "handler error"
                        else:
                            message = "request uri not callable"
                    else:
                        message = "request uri not exist"

                    client.send("HTTP/1.1 200 OK\r\n\r\n")
                    client.send("{\"code\":"+str(code)+",\"message\":\"" + message + "\"}")
                else:
                    client.send("HTTP/1.1 200 OK\r\n\r\n")
                    client.send("{\"code\":-1,\"message\":\"method not support\"}")
            except:
                print("exception but continue!")
            finally:
                try:
                    if client is not None:
                        client.close();
                except:
                    print("close error")

    def parseRequest(self, addr, content):
        if content != '':
            requestLines = content.split("\r\n");
            protoLine = requestLines[0];
            protoInfoArr = protoLine.split(" ");
            method = protoInfoArr[0];
            url = protoInfoArr[1];
            paramsMap = {}
            if url != "/":
                urlInfoArray = url.split("?");
                requestUri = urlInfoArray[0];
                if len(urlInfoArray) > 1:
                    params = urlInfoArray[1];
                    paramArr = params.split("&")
                    for i in range(0, len(paramArr)):
                        paramPair = paramArr[i].split("=")
                        paramsMap[paramPair[0]]=paramPair[1];
            else:
                requestUri = url;

            return method, requestUri, paramsMap;
