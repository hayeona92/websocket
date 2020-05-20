import asyncio
import os

import aiohttp.web
import time

HOST = os.getenv('HOST', '0.0.0.0')
PORT = 8080

async def websocket_handler(request):
    print('connection starting')
    start = time.time()
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('connection ready')
    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(msg.data)
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
    temp = time.time()-start
    print(temp)
    return (time.time()-start)


loop = asyncio.get_event_loop()
app = aiohttp.web.Application(loop=loop)
app.router.add_route('GET', '/ws', websocket_handler)
aiohttp.web.run_app(app, host=HOST, port=PORT)
