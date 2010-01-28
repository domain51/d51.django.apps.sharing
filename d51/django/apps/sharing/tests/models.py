from django.contrib.auth.models import User
from django.test import TestCase
from d51.django.apps.sharing.models import URL, Share, Sender
from d51.django.apps.sharing import services
import random
import mox

class TestOfURL(TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_of_share_to_service(self):
        url = URL()
        user = User.objects.create(
            username='gary%d'%random.randint(1,1000),
        ) 
        self.mox.StubOutWithMock(services, 'create_share')
        services.create_share('gary_service', user, from_url=url, with_post={})
        self.mox.ReplayAll()
        url.share_to_service('gary_service', user, {})
        self.mox.VerifyAll()

    def test_of_send(self):
        random_number = random.randint(1,1000)
        mock_share = self.mox.CreateMock(Share)
        mock_share.send(Sender).AndReturn(random_number)
        url = URL()
        user = User.objects.create(
            username='gary%d'%random.randint(1,1000),
        ) 
        self.mox.StubOutWithMock(services, 'create_share')
        services.create_share('gary_service', user, from_url=url, with_post={}).AndReturn(mock_share)
        self.mox.ReplayAll()
        self.assertEquals(random_number, url.send('gary_service', user, {}))
        self.mox.VerifyAll()

