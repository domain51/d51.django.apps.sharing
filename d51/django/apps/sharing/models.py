from django.db import models
from django.contrib.auth.models import User
from d51.django.apps.sharing import services
from d51.django.apps.sharing import providers 

class Sender(object):
    def __init__(self, share):
        self.share = share

    def prepare(self):
        if not self.share.alternate.is_fulfilled:    
            self.share.alternate.fulfill()
    def send(self):
        self.share.get_service().send_share(self.share)
        self.share.is_fulfilled = True
        self.share.save()

    def __call__(self):
        self.prepare()
        self.send()

class URL(models.Model):
    url = models.URLField()

    def send(self, service_name, from_user, with_post, with_sender_class=Sender):
        share = self.share_to_service(service_name, from_user, with_post)
        return share.send(with_sender_class)

    def share_to_service(self, service_name, from_user, post_data):
        return services.create_share(service_name, from_user, from_url=self, with_post=post_data)

class Alternate(models.Model):
    original_url = models.ForeignKey(URL, related_name='alternates') 
    url = models.URLField(null=True, blank=True)
    provider = models.CharField(max_length=255)

    @property
    def is_fulfilled(self):
        return bool(self.url) 

    def fulfill(self):
        providers.load_provider(self.provider).fulfill(self)

class Share(models.Model):
    alternate = models.ForeignKey(Alternate, related_name='shares')
    is_fulfilled = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    service = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def get_service(self):
        return services.load_service(self.service, self.alternate.original_url)

    def send(self, with_sender_class):
        if self.is_fulfilled:
            raise SomeBadError 
        return with_sender_class(self)()
