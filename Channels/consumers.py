import json
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from GAMES.models import Match, Game
from channels.db import database_sync_to_async

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # print(self.scope['url_route'])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
       
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        # self.send(text_data=json.dumps({
        #         'message': self.room_name
        #     }))
        

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        match = Match.objects.filter(id=self.room_name).first()
        # Send message to WebSocket
        self.send(text_data=json.dumps({
                "message":"update",
                "status": match.status,
                "id1":match.score_play1,
                "id2":match.score_play2
            }))



class Games(WebsocketConsumer):

    def connect(self):
        self.room_name = "match"
        self.room_group_name = "match"
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        try:
            result = text_data_json['result']
            match = text_data_json['match']
            if result == 0:
                self.send(text_data="{'result':'ok'}")
            elif result == 1:
                try:
                    temp = Match.objects.filter(id=match).first()
                    temp.status = 1
                    temp.save()
                    self.send(text_data="{'result':1}")
                except Exception as e:
                    print(e)
                    self.send(text_data="Error in "+str(e))
            elif result == 3:
                try:
                    temp = Match.objects.filter(id=match).first()
                    g = Game.objects.filter(id=temp.game_id).first()
                    g.status = 1
                    g.save()
                    temp.status = 2
                    temp.save()
                    try:
                        score1 = text_data_json['id1']
                        score2 = text_data_json['id2']
                        temp = Match.objects.filter(id=match).first()
                        temp.score_play1 = score1
                        temp.score_play2 = score2
                        temp.save()
                    except Exception as e:
                        self.send(text_data="Error in "+str(e))
                    self.send(text_data="{'result':1}")
                except Exception as e:
                    print(e)
                    self.send(text_data="Error in "+str(e))
            elif result == 2:
                try:
                    status = text_data_json['status']
                    score1 = text_data_json['id1']
                    score2 = text_data_json['id2']
                    temp = Match.objects.filter(id=match).first()
                    temp.status = status
                    temp.score_play1 = score1
                    temp.score_play2 = score2
                    temp.save()
                    self.send(text_data="{'result':1}")
                except Exception as e:
                    print(e)
                    self.send(text_data="Error in "+str(e))
        except Exception as e:
            print(e)
            self.send(text_data="Error in "+str(e))

        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': option
        #     }
        # )

    # def chat_message(self, event):
    #     # message = event['message']
    #     message ="hello"
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))
