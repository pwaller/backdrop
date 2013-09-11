import unittest
from backdrop.write import api
from backdrop.write.permissions import Permissions


class OauthTestCase(unittest.TestCase):
    def setUp(self):
        self.client = api.app.test_client()
        self.app = api.app

    def given_user_is_signed_in_as(self, name="testuser",
                                   email="testuser@example.com"):
        with self.client.session_transaction() as session:
            session["user"] = {
                "name": name,
                "email": email
            }

    def given_user_is_not_signed_in(self):
        with self.client.session_transaction() as session:
            if "user" in session:
                del session["user"]

    def given_bucket_permissions(self, email, buckets):
        self.app.permissions = Permissions({email: buckets})

    def given_user_is_signed_in_with_permissions(self, name, email, buckets):
        self.given_user_is_signed_in_as(name, email)
        self.given_bucket_permissions(email, buckets=buckets)
