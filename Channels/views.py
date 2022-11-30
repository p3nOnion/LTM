import asyncio

import websockets as websockets
from django.shortcuts import render
from threading import Thread
import threading
from django.core.exceptions import PermissionDenied
# Create your views here.

def lobby(request):
    return render(request, 'Channels/lobby.html')
def room(request, room_name):
    return render(request, 'Channels/room.html', {
        'room_name': room_name
    })
# async def handler(websocket):
#      print(1)
# async def main():
#     async with websockets.serve(handler, "127.0.0.1", 8881):
#         await asyncio.Future()  # run forever\
# try:
#     t1 = threading.Thread(target=asyncio.run(main()), args=(main(),))
#     t1.start()
# except Exception as e:
#     print(e)
#     pass
