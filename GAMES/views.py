import websockets
import asyncio
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http.response import FileResponse
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta, timezone, tzinfo
from django.contrib import messages as mmesg
from pwn import *
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
            game = Game(name=name, author_id=request.user.id, ip=ip, port=port, rule=rule)
            game.save()
        return redirect("accounts:profile")
    try:
        games = Game.objects.filter(author_id=request.GET['id'])
    except:
        games = Game.objects.all()
    form = MatchForm()
    users = Users.objects.all()
    return render(request, 'Games/games.html', {"games": games, "users": users, "form": form})


# def create_match(request):
#     if request.method == "POST":
#         form = MatchForm(request.POST)
#         if form.is_valid():
#             game = form.cleaned_data.get('game')
#             print(game)
#             id1 = form.cleaned_data.get('id_play1')
#             id2 = form.cleaned_data.get('id_play2')
#             password = form.cleaned_data.get('password')
#             Match(game=game, id_play1=id1, id_play2=id2, password=password, date_create=timezone.now)
#             return redirect("game:match_home")
#     form = MatchForm()
#     return render(request, "Games/match.html", {"form": form})


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
            if g.is_active==False:
                return  redirect("game:match_home")
            data = {
                "action": 1,
                "id1": id1,
                "id2": id2,
                "passwd": password
            }
            if g.ip[:5] == "ws://":
                start_time =int(time.time())
                async def connect():
                    async with websockets.connect(g.ip + ":" + str(g.port)) as websocket:
                        await websocket.send(json.dumps(data))
                        msg = await websocket.recv()# dang co bug o day
                        print(msg)
                        try:
                            message = msg['result']
                            ip_connect = msg['ip']
                            port_connect = msg['port']
                            path_connect = msg['path']
                            print(message)
                            if message == 1:
                                Match(game_id=int(game), id_play1=id1, id_play2=id2, password=password,
                                      date_create=datetime.now()).save()
                                mmesg.success(request, "Create a successful game")
                                Notification(title=g.name, user_id=id1, ip=ip_connect, port=port_connect,
                                             content="connect game %s with id match=%s, ip=%s, port=%s, path=%s" % (
                                                 g.name,
                                                 Match.objects.filter(game_id=int(game), id_play1=id1, id_play2=id2,
                                                                      password=password).first().id, ip_connect,
                                                 port_connect, path_connect))
                                Notification(title=g.name, user_id=id2, ip=ip_connect, port=port_connect,
                                             content="connect game %s with id match=%s, ip=%s, port=%s, path=%s" % (
                                                 g.name,
                                                 Match.objects.filter(game_id=int(game), id_play1=id1, id_play2=id2,
                                                                      password=password).first().id, ip_connect,
                                                 port_connect, path_connect))

                        except:
                            mmesg.error(request, "Can't create match")
                            # if int(time.time()) - start_time > 5:
                            websocket.close()
                        websocket.close()

                async def main():
                    MAX_TIMEOUT = 20
                    try:
                        await asyncio.wait_for(connect(), timeout=MAX_TIMEOUT)
                    except:
                        print('The task was cancelled due to a timeout')
                asyncio.run(main())
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
                                                                                                                Match.objects.filter(
                                                                                                                    game_id=int(
                                                                                                                        game),
                                                                                                                    id_play1=id1,
                                                                                                                    id_play2=id2,
                                                                                                                    password=password).first().id,
                                                                                                                ip_connect,
                                                                                                                port_connect,
                                                                                                                path_connect)).save()
                            Notification(title=g.name, user_id_id=id2, passwd=password, ip=ip_connect,
                                         port=port_connect,
                                         content="connect game %s with id match=%s, ip=%s, port=%s, path=%s" % (g.name,
                                                                                                                Match.objects.filter(
                                                                                                                    game_id=int(
                                                                                                                        game),
                                                                                                                    id_play1=id1,
                                                                                                                    id_play2=id2,
                                                                                                                    password=password).first().id,
                                                                                                                ip_connect,
                                                                                                                port_connect,
                                                                                                                path_connect)).save()


                    except:
                        mmesg.error(request, "Can't create match")
                    req.close()
                except:
                    mmesg.error(request, "Can't connect to ip %s port %s" % (g.ip, g.port))
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
    noti = Notification.objects.filter(user_id=request.user.id)
    return render(request, 'Games/notification.html', {"notis": noti})
