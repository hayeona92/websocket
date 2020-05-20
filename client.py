import asyncio
import os
import aiohttp

HOST = os.getenv('HOST', '0.0.0.0')
PORT = 8080

URL = f'http://{HOST}:{PORT}/ws'

async def main():
    session = aiohttp.ClientSession()
    async with session.ws_connect(URL) as ws:
        await prompt_and_send(ws)
        async for msg in ws:
            print('Message received from server:', msg)
            await prompt_and_send(ws)

            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                break

async def prompt_and_send(ws):
    new_msg_to_send = input('type message: ')
    if new_msg_to_send == 'exit':
        print('exit')
        raise SystemExit(0)
    await ws.send_str(new_msg_to_send)



print('exit = quit')
loop = asyncio.get_event_loop()
loop.run_until_complete(main())