import asyncio
import os

import aiohttp.web
import time

HOST = os.getenv('HOST', '0.0.0.0')
PORT = 8080


async def websocket_handler(request):
    print('connection starting')

    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('connection ready')

    timer_start = time.time()
    start = timer_start

    async for msg in ws:

        timer_end = time.time()
        result = timer_end - timer_start
        timer_start = timer_end
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(msg.data)
            if msg.data == 'close':
                res = time.time()-start
                await ws.send_str('total spent {} question number {}'.format(str(res),msg.data))
                await ws.close()
            else:
                await ws.send_str('problem spent {}'.format(str(result)))


    return ws


loop = asyncio.get_event_loop()
app = aiohttp.web.Application(loop=loop)
app.router.add_route('GET', '/ws', websocket_handler)
aiohttp.web.run_app(app, host=HOST, port=PORT)
