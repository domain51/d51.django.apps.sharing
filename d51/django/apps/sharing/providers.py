from d51.django.apps.sharing.utils import load_target_from_setting_with_key as load_target
from d51.django.apps.sharing.exceptions import ProviderNotImplemented
from django.conf import settings as django_settings

SHARING_PREFERRED_PROVIDER_KEY = 'D51_DJANGO_APPS_SHARING_PREFERRED_PROVIDER'
SHARING_PROVIDERS_SETTINGS_KEY = 'D51_DJANGO_APPS_SHARING_PROVIDERS'

class SharingProviderException(Exception):
    pass

class Provider(object):
    def __init__(self, name):
        self.name = name

    def create_alternate(self, from_url):
        return from_url.alternates.create(
            provider=self.name
        ) 

    def fulfill(self, alternate):
        alternate.url = alternate.original_url.url
        alternate.is_fulfilled = True
        alternate.save()
        return alternate

def load_provider(provider_name=None, settings=django_settings):
    if provider_name is None:
        provider_name = getattr(settings, SHARING_PREFERRED_PROVIDER_KEY) 
    return load_target(SHARING_PROVIDERS_SETTINGS_KEY, provider_name)(provider_name)
