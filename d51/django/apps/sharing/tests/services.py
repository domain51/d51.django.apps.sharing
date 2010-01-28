from django.contrib.auth.models import User
from django.test import TestCase
from d51.django.apps.sharing.models import URL, Alternate, Share
from d51.django.apps.sharing import services
from d51.django.apps.sharing import providers 
from django.db.models.query import QuerySet
import random
import mox
from django.conf import settings as django_settings
from d51.django.apps.sharing.utils import load_target_from_setting_with_key as load_target

class TestOfServiceObject(TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_of_init(self):
        name = 'rand-%d' % random.randint(1,1000)
        random_provider = 'rand-prov-%d' % random.randint(1,1000)
        fake_url = URL()
        fake_settings = object()
        self.mox.ReplayAll()
        service = services.Service(name, fake_url, random_provider)
        self.assertEqual(service.name, name)
        self.assertEqual(service.url, fake_url)
        self.assertEqual(service.provider, random_provider)
        self.mox.VerifyAll()

    def test_of_find_available_alternates(self):
        random_result = 'rand-%d' % random.randint(1,1000)
        provider = providers.Provider("provider_name")

        url = self.mox.CreateMock(URL)
        url.alternates = self.mox.CreateMock(Alternate.objects.__class__)
        url.alternates.filter(provider=provider.name).AndReturn(random_result)
        service = services.Service('servicename', url, provider) 
        self.mox.ReplayAll()
        service.find_available_alternates()
        self.mox.VerifyAll()

    def test_of_create_share_with_no_existing_alternate(self):
        user = User.objects.create(
            username='random-%d'%random.randint(1,1000)
        )
        random_name = 'rand-%d'%random.randint(1,1000)
        service_random_name = 'rand-%d'%random.randint(1,1000)
        provider = providers.Provider(random_name)

        fake_form = self.mox.CreateMock(type)
        fake_form_instance = self.mox.CreateMock(services.ServiceForm)
        fake_form.__call__({}).AndReturn(fake_form_instance)
        fake_form_instance.is_valid().AndReturn(True)
        fake_form_instance.contrib_dict_to_share().AndReturn({})

        mock_alternate = self.mox.CreateMock(Alternate)
        mock_alternate.shares = self.mox.CreateMock(Share.objects.__class__)

        url = self.mox.CreateMock(URL)
        url.alternates = self.mox.CreateMock(Alternate.objects.__class__)
        url.alternates.filter(provider=provider.name).AndReturn(None)
        url.alternates.create(provider=provider.name).AndReturn(mock_alternate)
        mock_alternate.shares.create(user=user, service=service_random_name)

        service = services.Service(service_random_name, url, provider)
        self.mox.ReplayAll()
        service.create_share(user, {}, fake_form)
        self.mox.VerifyAll()

    def test_of_create_share_with_existing_alternate(self):
        user = User.objects.create(
            username='random-%d'%random.randint(1,1000)
        )
        random_name = 'rand-%d'%random.randint(1,1000)
        service_random_name = 'rand-%d'%random.randint(1,1000)
        provider = providers.Provider(random_name)

        fake_form = self.mox.CreateMock(type)
        fake_form_instance = self.mox.CreateMock(services.ServiceForm)
        fake_form.__call__({}).AndReturn(fake_form_instance)
        fake_form_instance.is_valid().AndReturn(True)
        fake_form_instance.contrib_dict_to_share().AndReturn({})
        mock_alternate = self.mox.CreateMock(Alternate)
        mock_alternate.shares = self.mox.CreateMock(Share.objects.__class__)

        mock_queryset = self.mox.CreateMock(QuerySet)
        mock_queryset[0].AndReturn(mock_alternate)

        url = self.mox.CreateMock(URL)
        url.alternates = self.mox.CreateMock(Alternate.objects.__class__)
        url.alternates.filter(provider=provider.name).AndReturn(mock_queryset)


        mock_alternate.shares.create(user=user, service=service_random_name)

        service = services.Service(service_random_name, url, provider)
        self.mox.ReplayAll()
        service.create_share(user, {}, fake_form)
        self.mox.VerifyAll()

    def test_unimplemented(self):
        service = services.Service('anything', URL(), providers.Provider('also-anything'))
        self.assertRaises(services.ServiceNotImplemented, service.send_share, share='additionally, anything') 

class TestOfServiceFunctions(TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_of_load_service(self):
        self.mox.StubOutWithMock(services, 'load_target')
        self.mox.StubOutWithMock(providers, 'load_provider')
        random_name = 'random-name-%d'%random.randint(1,1000)
        mock_service = self.mox.CreateMock(services.Service) 
        services.load_target(services.SHARING_SERVICES_SETTINGS_KEY, random_name).AndReturn(mock_service.__class__)
        providers.load_provider.__call__().AndReturn(None)
        self.mox.ReplayAll()

        fake_url = URL()
        results = services.load_service(random_name, fake_url)
        
        self.assertEquals(results.name, random_name)
        self.assertEquals(results.url, fake_url)
        self.assertEquals(results.provider, None)
        self.mox.VerifyAll()

    def test_of_create_share(self):
        random_name = 'random-name-%d'%random.randint(1,1000)
        mock_service = self.mox.CreateMock(services.Service) 
        mock_url = self.mox.CreateMock(URL)
        mock_user = self.mox.CreateMock(User)
        self.mox.StubOutWithMock(services, 'load_service')
        services.load_service(random_name, mock_url).AndReturn(mock_service)
        mock_service.create_share(mock_user, mock_url, {}).AndReturn(random_name)
        self.mox.ReplayAll()
        results = services.create_share(random_name, mock_user, mock_url, {})
        self.assertEqual(results, random_name)
        self.mox.VerifyAll()
        
