# echo-server.py

import websockets
import asyncio
import json
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


msg = {"result": 1, "ip": "localhost", "port": 10010, "path": "path"}


msg2 = {"result": 0}


data = {
    "action": 1,
    "match": 12,
    "id1": id1,
    "id2": id2,
    "passwd": password
}


async def create(websocket):
    async for message in websocket:
        data = json.loads(message)
        print(data)
        if data["action"] == 1:
            await websocket.send(json.dumps(msg))
        else:
            await websocket.send(json.dumps(msg2))


async def server():
    async with websockets.serve(create, "104.194.240.16", 8881):
        await asyncio.Future()
asyncio.run(server())
