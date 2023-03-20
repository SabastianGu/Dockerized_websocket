from channels.testing import WebsocketCommunicator
from django.test import TestCase
from engine_side.consumers import TheConsumer
import math

class TestTheConsumer(TestCase):
    async def test_calculate_factorial(self):
        communicator = WebsocketCommunicator(TheConsumer.as_asgi(), "/ws/")
        await communicator.connect()
        message = {
            'action': 'calculate',
            'value': 5,
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        self.assertEqual(response['result'], math.factorial(5))
        await communicator.disconnect()

    async def test_invalid_input(self):
        communicator = WebsocketCommunicator(TheConsumer.as_asgi(), "/ws/")
        await communicator.connect()
        message = {
            'action': 'calculate',
            'value': 'not an integer',
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        self.assertIn('error', response)
        await communicator.disconnect()

    async def test_invalid_action(self):
        communicator = WebsocketCommunicator(TheConsumer.as_asgi(), "/ws/")
        await communicator.connect()
        message = {
            'action': 'invalid action',
            'value': 'whatever',
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        self.assertIn('error', response)
        await communicator.disconnect()

    async def test_multiple_requests(self):
        communicator = WebsocketCommunicator(TheConsumer.as_asgi(), "/ws/")
        await communicator.connect()
        messages = [
            {
                'action': 'calculate',
                'value': 4,
            },
            {
                'action': 'calculate',
                'value': 6,
            },
            {
                'action': 'calculate',
                'value': 2,
            },
        ]
        expected_results = [math.factorial(m['value']) for m in messages]
        for message in messages:
            await communicator.send_json_to(message)
        for expected_result in expected_results:
            response = await communicator.receive_json_from()
            self.assertEqual(response['result'], expected_result)
        await communicator.disconnect()