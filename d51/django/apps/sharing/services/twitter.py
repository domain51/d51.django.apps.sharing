from ..services import Service, ServiceForm
from d51.django.auth.twitter import utils
from django import forms

class TwitterForm(ServiceForm):
    message = forms.CharField(max_length=120, widget=forms.widgets.Textarea)

    def contrib_dict_to_share(self):
        return { 'title':self.cleaned_data['message'] }

class TwitterService(Service):
    def get_form_class(self):
        return TwitterForm

    def send_share(self, share):
        api = utils.get_twitter_api(token=share.user.twitter.get_oauth_token())

        message = '%s %s' % (share.title, share.alternate.url)
        api.statuses.update.POST(status=message) 
