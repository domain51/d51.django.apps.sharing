from django.contrib.auth.models import User
from django.test import TestCase
from d51.django.apps.sharing.models import URL, Alternate, Share
from d51.django.apps.sharing import services
from dolt import Dolt
from d51.django.apps.sharing import providers 
from django.db.models.query import QuerySet
import random
import mox
from django.conf import settings as django_settings
from d51.django.apps.sharing.utils import load_target_from_setting_with_key as load_target

class EasyRandom(object):
    @property
    def random(self):
        if getattr(self, '_random', None) is not None:
            del self._random
        return random.randint(1,100)

    @property
    def random_string(self):
        if getattr(self, '_random_string', None) is not None:
            del self._random_string
        return 'rand-%d'%self.random
_ = EasyRandom()


class TestOfServiceObject(TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_of_init(self):
        name = 'rand-%d' % _.random
        random_provider = 'rand-prov-%d' % _.random
        fake_url = URL()
        fake_settings = object()
        self.mox.ReplayAll()
        service = services.Service(name, fake_url, random_provider)
        self.assertEqual(service.name, name)
        self.assertEqual(service.url, fake_url)
        self.assertEqual(service.provider, random_provider)
        self.mox.VerifyAll()

    def test_of_find_available_alternates(self):
        random_result = 'rand-%d' % _.random
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
            username='random-%d'%_.random
        )
        random_name = 'rand-%d'%_.random
        service_random_name = 'rand-%d'%_.random
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
            username='random-%d'%_.random
        )
        random_name = 'rand-%d'%_.random
        service_random_name = 'rand-%d'%_.random
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
        random_name = 'random-name-%d'%_.random
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
        random_name = 'random-name-%d'%_.random
        mock_service = self.mox.CreateMock(services.Service) 
        mock_url = self.mox.CreateMock(URL)
        mock_user = self.mox.CreateMock(User)
        self.mox.StubOutWithMock(services, 'load_service')
        services.load_service(random_name, mock_url).AndReturn(mock_service)
        mock_service.create_share(mock_user, {}).AndReturn(random_name)
        self.mox.ReplayAll()
        results = services.create_share(random_name, mock_user, mock_url, {})
        self.assertEqual(results, random_name)
        self.mox.VerifyAll()

from ..services.facebook import FacebookService, FacebookForm
from ..services.twitter import TwitterService, TwitterForm 

class TestOfTwitterService(TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_of_get_form_class(self):
        service = TwitterService(None, None, None)
        self.assertEqual(service.get_form_class(), TwitterForm)

    def test_of_send_share(self):
        from d51.django.auth.twitter import utils, models

        random_value = _.random
        random_string = 'random thing to say no. %d' % _.random

        user = User.objects.create(
            username='rand-%d'%_.random
        )
        user.twitter = self.mox.CreateMock(models.TwitterToken)
        user.twitter.get_oauth_token().AndReturn(random_value)

        alternate = Alternate()
        alternate.url = random_string

        share = Share()
        share.alternate = alternate
        share.user = user
        share.title = random_string

        dolt_mock = self.mox.CreateMock(Dolt)
        dolt_mock.statuses = self.mox.CreateMock(Dolt)
        dolt_mock.statuses.update = self.mox.CreateMock(Dolt)
        dolt_mock.statuses.update.POST = self.mox.CreateMock(Dolt)
        dolt_mock.statuses.update.POST(status='%s %s' % (share.title, random_string))
        self.mox.StubOutWithMock(utils, 'get_twitter_api')
        utils.get_twitter_api(token=random_value).AndReturn(dolt_mock)

        self.mox.ReplayAll()
        service = TwitterService(None, None, None)
        service.send_share(share)
        self.mox.VerifyAll()
        
class TestOfFacebookService(TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_of_get_form_class(self):
        service = FacebookService(None, None, None)
        self.assertEqual(service.get_form_class(), FacebookForm)

    def test_send_share(self):
        from d51.django.auth.facebook import utils, models

        user = User.objects.create(
            username=_.random_string
        )
        user.facebook = models.FacebookID()
        user.facebook.uid = _.random
        self.mox.StubOutWithMock(utils, 'get_facebook_api')

        alternate = Alternate()
        alternate.url = _.random_string

        share = Share()
        share.user = user
        share.alternate = alternate
        share.title, share.description = _.random_string, _.random_string

        fake_attachment = {
            'name':share.title,
            'href':share.alternate.url,
            'description':share.description
        }

        mock_facebook = self.mox.CreateMock(Dolt)
        mock_facebook.stream = self.mox.CreateMock(Dolt)
        mock_facebook.stream.publish = self.mox.CreateMock(Dolt)
        mock_facebook.stream.publish(attachment=fake_attachment, uid=str(user.facebook.uid))
        utils.get_facebook_api(for_uid=user.facebook.uid).AndReturn(mock_facebook)
        self.mox.ReplayAll()
        service = FacebookService(None, None, None)
        service.send_share(share)
        self.mox.VerifyAll()
