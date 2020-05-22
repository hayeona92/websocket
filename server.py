import asyncio
import time
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import json


class MyServerProtocol(WebSocketServerProtocol):
    working_on = False
    options = ['a','b','c','d','e','f','g']
    start = 0
    end = 0
    async def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    async def onOpen(self):
        print("WebSocket connection open.")

    async def onMessage(self, payload, isBinary):
        if not isBinary:
            received_data = json.loads(payload.decode('utf8'))
            if not self.working_on:
                if received_data['question'].isnumeric():
                    self.working_on = True
                    self.start = time.time()
                    self.sendMessage(json.dumps(received_data).encode('utf8'))
                else: pass
            elif received_data['answer'] in self.options:
                self.end = time.time()
                print(self.end-self.start)
                self.working_on =False
            else:
                pass
    async def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    factory = WebSocketServerFactory("ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
