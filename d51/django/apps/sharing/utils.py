from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.conf import settings as django_settings

def load_target_from_module(location):
    try:
        get_module_and_target = lambda x: x.rsplit('.', 1)
        module, target = get_module_and_target(location)
        module = import_module(module)
        target = getattr(module, target, None)
        if target is None:
            raise ImproperlyConfigured('%s is not defined in %s' % get_module_and_target(location)) 
        return target
    except ImportError as e:
        raise ImproperlyConfigured('Error loading sharing setting %s: "%s"' % (location, e)) 

def load_target_from_setting_with_key(setting, key, settings=django_settings):
    location = getattr(settings, setting, {}).get(key, None)
    if location is None:
        raise ImproperlyConfigured('Could not load key %s from %s' % (key, setting))
    return load_target_from_module(location) 
