from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User

from engine_side.middleware import JwtAuthMiddlewareStack
from engine_side.consumers import TheConsumer

from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async


class TestTokenAuthMiddleware(TestCase):
    async def test_middleware_with_valid_token(self):
        user = await database_sync_to_async(User.objects.create_user)('testuser', password='testpass')
        token = user.token()  # Create a valid JWT token for the user

        
        application = JwtAuthMiddlewareStack(TheConsumer.as_asgi())
        communicator = WebsocketCommunicator(application, '/test/')
        connected, _ = await communicator.connect(
            headers=[(b'sec-websocket-protocol', b'graphql-ws'), (b'cookie', f'token={token}'.encode())]
        )
        self.assertTrue(connected)

        # Проверка scope
        response = await communicator.receive_json_from()
        self.assertEqual(response.get('type'), 'websocket.accept')
        self.assertEqual(response.get('user').get('username'), 'testuser')

        await communicator.disconnect()

    async def test_middleware_with_invalid_token(self):
        # Create a test communicator and connect to the websocket with an invalid token in the query string
        application = JwtAuthMiddlewareStack(TheConsumer.as_asgi())
        communicator = WebsocketCommunicator(application, '/test/?token=invalid_token')
        connected, _ = await communicator.connect(headers=[(b'sec-websocket-protocol', b'graphql-ws')])
        self.assertTrue(connected)

        # Verify that an anonymous bro is set in the scope
        response = await communicator.receive_json_from()
        self.assertEqual(response.get('type'), 'websocket.accept')
        self.assertIsInstance(response.get('user'), AnonymousUser)

        await communicator.disconnect()