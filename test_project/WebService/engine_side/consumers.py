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
    CALCULATE_ACTION = 'calculate'
    PERFECT_ACTION = 'Check if number is perfect'
    async def connect(self):
        try:
            await self.accept()
        except Exception as e:
            print(f"Failed to connect to WebSocket: {e}")

    async def disconnect(self, close_code):
        try:
            await self.close()
        except Exception as e:
            print(f"Failed to disconnect from WebSocket: {e}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            response = {'error':"Invalid data format. Please, try again"}
            await self.send(json.dumps(response))
        action = data.get('action')
        value = data.get('value')

        if action == self.CALCULATE_ACTION:
                try:
                    number = int(value)
                    result = math.factorial(number)
                    response = {'result': result}
                except ValueError:
                    response = {'error': 'Invalid input'}
        elif action == self.PERFECT_ACTION:
                try:
                    number = int(value)
                    result, explanation = self.calculate_perfect_number(number)
                    response = {'result': result, 'explanation': explanation}
                except ValueError:
                    response = {'error': 'Invalid input'}
        else:
            response = {'error': 'Invalid action'}

        await self.send(json.dumps(response))

    def calculate_perfect_number(self, number):
        if number <= 0:
            raise ValueError("Number must be positive")

        factors = [i for i in range(1, number) if number % i == 0]
        if sum(factors) == number:
            return number, f"{number} is a perfect number"

        i = 1
        while True:
            candidate = number + i
            factors = [j for j in range(1, candidate) if candidate % j == 0]
            if sum(factors) == candidate:
                return candidate, f"{number} is not a perfect number, but the nearest perfect number is {candidate}"
            i += 1

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
