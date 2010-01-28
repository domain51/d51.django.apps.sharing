from d51.django.apps.sharing.utils import load_target_from_setting_with_key as load_target
from django.conf import settings as django_settings
from django import forms
from ..exceptions import ServiceNotImplemented
SHARING_SERVICES_SETTINGS_KEY = 'D51_DJANGO_APPS_SHARING_SERVICES'

class SharingServiceException(Exception):
    pass

class SharingServiceInvalidForm(SharingServiceException):
    pass

class ServiceForm(forms.Form):
    def contrib_dict_to_share(self):
        raise ServiceNotImplemented

class Service(object):
    def __init__(self, name, for_url, provider):
        self.name = name
        self.url = for_url
        self.provider = provider 

    def find_available_alternates(self):
        return self.url.alternates.filter(provider=self.provider.name)

    def get_form_class(self):
        raise ServiceNotImplemented

    def get_parsed_form_data(self, valid_form):
        raise ServiceNotImplemented

    def create_share(self, from_user, with_post, override_form_class=None):
        available_alternates = self.find_available_alternates()
        alternate = available_alternates[0] if available_alternates else self.provider.create_alternate(self.url)
        form_class = self.get_form_class() if not override_form_class else override_form_class 
        form = form_class(with_post)
        if form.is_valid():
            return alternate.shares.create(
                user=from_user,
                service=self.name,
                **form.contrib_dict_to_share()
            )  
        raise SharingServiceInvalidForm()

    def send_share(self, share):
        raise ServiceNotImplemented

def load_service(service_name, from_url):
    from ..providers import load_provider

    provider = load_provider()
    return load_target(SHARING_SERVICES_SETTINGS_KEY, service_name)(service_name, from_url, provider)

def create_share(service_name, from_user, from_url, with_post):
    service = load_service(service_name, from_url)
    return service.create_share(from_user, with_post)
