import jwt
from django.test import TestCase
from ws_test import settings
from engine_side.tokening import create_access_token, create_token, ALGORITHM
import datetime
from datetime import timedelta

class JWTTestCase(TestCase):

    def test_create_access_token(self):
        
        test_data = {"user_id": 123}
        access_token_exp = timedelta(minutes=60)
        encoded_jwt = create_access_token(test_data, access_token_exp)
        decoded_jwt = jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(decoded_jwt["user_id"], test_data["user_id"])
        self.assertTrue(datetime.utcnow() < datetime.fromtimestamp(decoded_jwt["exp"]))

    def test_create_token(self):
        test_user_id = 123
        token = create_token(test_user_id)
        self.assertIn("access_token", token)
        self.assertIn("token_type", token)
        self.assertEqual(token["token_type"], "Token")
        decoded_jwt = jwt.decode(token["access_token"], settings.SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(decoded_jwt["user_id"], test_user_id)
        self.assertTrue(datetime.utcnow() < datetime.fromtimestamp(decoded_jwt["exp"]))

