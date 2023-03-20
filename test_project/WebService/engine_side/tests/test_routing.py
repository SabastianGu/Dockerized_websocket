from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.urls import path, re_path
from engine_side import consumers, routing
from django.test import TestCase


class TestWebsocketRouting(TestCase):
    async def test_the_consumer_routing(self):
        application = URLRouter(routing.websocket_urlpatterns)
        communicator = WebsocketCommunicator(application, '/ws/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_user_consumer_routing(self):
        application = URLRouter(routing.websocket_urlpatterns)
        communicator = WebsocketCommunicator(application, '/ws/endpoint/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()


