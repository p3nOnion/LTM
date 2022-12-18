import websockets
import asyncio
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from asgiref.sync import sync_to_async, async_to_sync
from datetime import datetime, timedelta, timezone, tzinfo
from django.contrib import messages as mmesg
from pwn import *
import random
import json

# Create your views here.
from GAMES.models import Game, Match, Notification
from Accounts.models import Users
from django.core.exceptions import PermissionDenied
from .forms import NewGameForm, MatchForm
import json


def home(request):
    noti = Notification.objects.filter(user_id=request.user.id)
    return render(request, 'Games/home.html', {"notis": noti})


def games(request):
    if request.method == "POST":
        form = NewGameForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            ip = form.cleaned_data.get("ip")
            port = form.cleaned_data.get("port")
            rule = form.cleaned_data.get("rule")
            game = Game(name=name, author_id=request.user.id,
                        ip=ip, port=port, rule=rule)
            game.save()
        return redirect("accounts:profile")
    try:
        games = Game.objects.filter(author_id=request.GET['id'])
    except:
        games = Game.objects.all()
    form = MatchForm()
    users = Users.objects.all()
    return render(request, 'Games/games.html', {"games": games, "users": users, "form": form})


def match(request, id):
    match = Match.objects.filter(id=id).first()
    return render(request, 'Games/id.html', {
        'id': id,
        'match':match
    })


def delete_game(request, id):
    author = Game.objects.filter(id=id).first()
    if author != None:
        if request.user.is_superuser or (int(request.user.id) == int(Game.objects.filter(id=id).first().author_id)):
            Game.objects.filter(id=id).delete()
            return redirect("accounts:profile")
        else:
            raise PermissionDenied
    return render(request, 'Games/home.html')


def match_home(request):
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            game = form.cleaned_data.get('game')
            id1 = form.cleaned_data.get('id_play1')
            id2 = form.cleaned_data.get('id_play2')
            if id1 == id2:
                mmesg.error(request, "2 users cannot overlap")
                return redirect("game:match_home")
            password = form.cleaned_data.get('password')
            g = Game.objects.filter(id=game).first()
            if g.status == 0:
                return redirect("game:match_home")
            match_id = Match.objects.all().order_by("-id").first().id
            match_id+=1
            data = {
                "action": 1,
                "match": match_id,
                "id1": id1,
                "id2": id2,
                "passwd": password
            }
            if g.ip[:5] == "ws://":
                try:
                    async def connect():
                        uri = g.ip + ":" + str(g.port)
                        async with websockets.connect(uri) as websocket:
                            async def send_hello():
                                # await asyncio.sleep(3)
                                await websocket.send(json.dumps(data))
                                # msg = (await json.loads(websocket.recv()))
                                # print(msg)

                            task = asyncio.create_task(send_hello())
                            msg = (await websocket.recv())
                            msg = json.loads(msg)
                            print(msg)
                            result = msg['result']
                            ip_connect = msg['ip']
                            port_connect = msg['port']
                            path_connect = msg['path']

                            if result == 1:
                                sync_to_async(Match(game_id=int(game), id_play1=id1, id_play2=id2, password=password,
                                                    date_create=datetime.now()).save())
                                mmesg.success(
                                    request, "Create a successful game")
                                sync_to_async(
                                    Notification(title=g.name, user_id_id=id1, ip=ip_connect, port=port_connect,
                                                 content="connect game %s with id match=%s, ip=%s, port=%s, path=%s" % (
                                                     g.name,
                                                     match_id, ip_connect,
                                                     port_connect, path_connect)).save())
                                sync_to_async(
                                    Notification(title=g.name, user_id_id=id2, ip=ip_connect, port=port_connect,
                                                 content="connect game %s with id match=%s, ip=%s, port=%s, path=%s" % (
                                                     g.name, match_id, ip_connect,
                                                     port_connect, path_connect)).save())
                            await task

                    asyncio.run(connect())
                    g.status = 0
                    g.save()

                except Exception as e:
                    print(e)
                    pass

            else:
                try:
                    req = remote(g.ip, g.port)
                    req.send(json.dumps(data).encode())
                    msg = json.loads(req.recv(1024).decode())
                    print(msg)
                    try:
                        message = msg['result']
                        ip_connect = msg['ip']
                        port_connect = msg['port']
                        path_connect = msg['path']
                        if message == 1:
                            Match(game_id=int(game), id_play1=id1, id_play2=id2, password=password,
                                  date_create=datetime.now()).save()
                            mmesg.success(request, "Create a successful game")
                            Notification(title=g.name, user_id_id=id1, passwd=password, ip=ip_connect,
                                         port=port_connect,
                                         content="connect game %s with id match=%s, ip=%s, port=%s, path=%s" % (g.name,
                                                                                                                match_id,
                                                                                                                ip_connect,
                                                                                                                port_connect,
                                                                                                                path_connect)).save()
                            Notification(title=g.name, user_id_id=id2, passwd=password, ip=ip_connect,
                                         port=port_connect,
                                         content="connect game %s with id match=%s, ip=%s, port=%s, path=%s" % (g.name,
                                                                                                                match_id,
                                                                                                                ip_connect,
                                                                                                                port_connect,
                                                                                                                path_connect)).save()

                        g.status = 0
                        g.save()
                        req.close()
                    except:
                        req.close()
                        mmesg.error(request, "Can't create match")
                    req.close()
                except:
                    mmesg.error(
                        request, "Can't connect to ip %s port %s" % (g.ip, g.port))
            return redirect("game:match_home")
    form = MatchForm()
    matchs = Match.objects.all().order_by("-date_create")
    try:
        matchs = matchs.filter(status=request.GET['type'])
    except:
        pass
    try:
        matchs = matchs.filter(game=request.GET['id'])
    except:
        pass
    for match in matchs:
        if match.status == 1:
            try:
                start = time.time()
                ip = Game.objects.filter(id=match.game_id).first().ip
                port = Game.objects.filter(id=match.game_id).first().port

                data = {
                    "result": 2,  # result = 3 là thông báo ván đấu kết thúc
                    # match sẽ là giá trị thông tin của match nào mà WS gửi lúc yêu cầu tạo match
                    "match": match.id,
                }
                if ip[:5] == "ws://":
                    address = f'%s:%s/' % (ip, port)
                    try:
                        async def hello():
                            async with websockets.connect(address) as websocket:
                                await websocket.send(json.dumps(data))
                    

                        asyncio.run(hello())
                        if time.time() - start:
                            break
                    except Exception as e:
                        print(e)
                        break
                else:
                    req = remote(ip, port)
                    req.send(json.dumps(data).encode())
                    req.close()
                    if time.time()-start:
                        break
            except:
                pass
    paginator = Paginator(matchs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    games = Game.objects.all()
    return render(request, 'Games/match.html', {"matchs": matchs, 'page_obj': page_obj, "games": games, "form": form})


def delete_noti(request, id):
    noti = Notification.objects.filter(id=id).first()
    if noti != None:
        if request.user.is_superuser or (
                int(request.user.id) == int(Notification.objects.filter(id=id).first().user_id_id)):
            Notification.objects.filter(id=id).delete()
        else:
            raise PermissionDenied
    noti = Notification.objects.filter(user_id=request.user.id)
    return render(request, 'Games/notification.html', {"notis": noti})


def scores(requeset):
    return render(requeset, template_name="Games/scores.html")


def index(requeset):
    return render(requeset, template_name="index.html")


def notification(request):
    noti = Notification.objects.filter(user_id=request.user.id).order_by('-id')
    return render(request, 'Games/notification.html', {"notis": noti})
