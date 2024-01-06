'''
This test file is a reproduction of a bug with the aiohttp library and Linux.
It's reported and the great team is trying to fix it at this moment.
This file will be used to see if the bug is fixed or not.
'''

import aiohttp
from aiohttp import ClientSession

import asyncio

url = "wss://demo.piesocket.com/v3/channel_123"

ws_headers = {
    'Origin': 'https://www.piesocket.com',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    'Sec-WebSocket-Version': '13',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.212 Safari/537.36',
}

async def run_init_conversation(prompt="hello world!", cookies = ''):
    async with ClientSession(headers=ws_headers, cookies=cookies, timeout=aiohttp.ClientTimeout(total=60)) as session:
        async with session.ws_connect(url, autoping=False, params={'api_key': "VCXCEuvhGcBDP7XhiJJUDvR1e1D3eiVjgZ9VRiaV"}) as wss:
            print("Connected to test")


if __name__ == '__main__':
    asyncio.run(run_init_conversation())