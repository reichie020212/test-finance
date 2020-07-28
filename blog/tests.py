from django.test import TestCase
from blog.models import UserInfo
from django.contrib.auth.models import User


class BasicTest(TestCase):
    def test_fields(self):
        user = User.objects.create(username='test-1')
        user_info = UserInfo()
        user_info.user = user
        user_info.first_name = 'first_name'
        user_info.last_name = 'last_name'
        user_info.middle_name = 'middle_name'
        user_info.gender = 'male'
        user_info.occupation = 'developer'
        user_info.save()

        record = UserInfo.objects.get(pk=1)
        self.assertEqual(record, user_info)
        user_info.delete()
        user.delete()
