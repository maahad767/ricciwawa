from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTest(TestCase):

    def test_create_user_with_uid_successful(self):
        """
        Test creating a new user with an email is successful
        """
        uid = 'testuiduser'
        get_user_model().objects.create_user(uid=uid)
        last_user = get_user_model().objects.latest('id')
        self.assertEqual(last_user.uid, uid)


