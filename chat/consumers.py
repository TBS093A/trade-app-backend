from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Lobby

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        checkSave = False
        for lobby in Lobby.objects.all():
            if lobby.name == self.room_name:
                lobby.userCount = lobby.userCount + 1
                Lobby.save(lobby)
                checkSave = True
                break
        if checkSave == False:
            lobbyRegister = Lobby()
            lobbyRegister.name= self.room_name
            lobbyRegister.userCount = 1
            Lobby.save(lobbyRegister)
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):

        updateCountOfUsers = Lobby.objects.get(name = self.room_name)
        updateCountOfUsers.userCount = updateCountOfUsers.userCount - 1
        if updateCountOfUsers.userCount == 0:
            Lobby.delete(updateCountOfUsers)
        else:
            Lobby.save(updateCountOfUsers)

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))