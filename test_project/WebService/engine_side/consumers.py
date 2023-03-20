from channels.generic.websocket import AsyncWebsocketConsumer
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ws_test.settings')
django.setup()

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins

from .models import User
from .serializers import UserSerializer
import json

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import math

class TheConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']
        value = data['value']

        if action == 'calculate':
            try:
                number = int(value)
                result = math.factorial(number)
                response = {'result': result}
            except ValueError:
                response = {'error': 'Invalid input'}
        else:
            response = {'error': 'Invalid action'}

        await self.send(json.dumps(response))

class UserConsumer(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.PatchModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        mixins.DeleteModelMixin,
        GenericAsyncAPIConsumer,
):

    queryset = User.objects.all()
    serializer_class = UserSerializer