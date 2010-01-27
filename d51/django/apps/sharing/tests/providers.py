from django.contrib.auth.models import User
from django.test import TestCase
from d51.django.apps.sharing.models import URL, Alternate, Share
from d51.django.apps.sharing import services, providers
import random
import mox


class TestOfProviderClass(TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_of_init(self):
        random_name = 'rand-%d'%random.randint(1,100)
        self.assertEqual(providers.Provider(random_name).name, random_name)

    def test_of_create_alternate(self):
        random_name = 'rand-%d'%random.randint(1,100)
        random_value = random.randint(1,100)
        mock_url = self.mox.CreateMock(URL)
        mock_url.alternates = self.mox.CreateMock(Alternate.objects)
        mock_url.alternates.create(
            provider=random_name
        ).AndReturn(random_value)
        self.mox.ReplayAll()
        self.assertEqual(providers.Provider(random_name).create_alternate(mock_url), random_value)
        self.mox.VerifyAll()

class TestOfProviderFunctions(TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_of_load_provider(self):
        mock_provider_class = self.mox.CreateMock(providers.Provider.__class__)
        self.mox.StubOutWithMock(providers, 'load_target')
        random_name = 'random-name-%d'%random.randint(1,1000)
        
        providers.load_target(providers.SHARING_PROVIDERS_SETTINGS_KEY, random_name).AndReturn(mock_provider_class)
        mock_provider_class(random_name)

        self.mox.ReplayAll()
        results = providers.load_provider(random_name)
        self.mox.VerifyAll()
