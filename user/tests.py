from django.test import TestCase
from user.models import User
from static_methods.sentMail import send_resetpassword_bymail


class UserTest(TestCase):

    def setUp(self):
        User.objects.create_user(email="test@email.com",
                                 username="test",
                                 first_name="user",
                                 last_name="user")

    def test_createUserAccount(self):
        user = User.objects.get(first_name="user")

        self.assertEqual(user.first_name, "user", msg="Success create user object")
        print("Success create user object")

    def test_sendEmail(self):
        self.assertTrue(send_resetpassword_bymail(to_email="ahmedjarada@hotmail.com", PIN='1234'),
                        msg="Success sent email")
        print("Success mailing SMTP")
