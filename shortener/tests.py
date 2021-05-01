from django.contrib.auth import get_user_model
from django.test import TestCase

from shortener import utils
from shortener.models import UrlRecord

User = get_user_model()


class UrlRecordModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="demo", password="demo")

    def test_user_created(self):
        usercount = User.objects.all().count()
        demouser = User.objects.first()
        self.assertEqual(demouser, self.user)
        self.assertEqual(usercount, 1)
        self.assertEqual(demouser.username, "demo")

    def test_urlrecord_created(self):
        demouser = User.objects.first()
        timefuture = utils.get_date_one_week_from_today()
        inputurl = "http://www.google.com"
        url = UrlRecord.objects.create(
            original_url=inputurl,
            user=demouser,
            short_url=utils.get_random_generated_shortcode,
            date_expiry=timefuture
        )
        self.assertEqual(url.original_url, inputurl)
        self.assertLess(url.date_created, url.date_expiry)
        self.assertEqual(url.user.username, "demo")
