from django import forms
from ..services import Service, ServiceForm
from d51.django.auth.facebook.utils import get_facebook_api
from django.utils import simplejson

class FacebookForm(ServiceForm):
    title = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, widget=forms.widgets.Textarea)
    def contrib_dict_to_share(self):
        return { 'title':self.cleaned_data['title'], 'description':self.cleaned_data['description'], }

class FacebookService(Service):
    def get_form_class(self):
        return FacebookForm

    def send_share(self, share):
        facebook_id = share.user.facebook.uid
        facebook_api = get_facebook_api(for_uid=share.user.facebook.uid)

        attachment = {
            'name':share.title,
            'href':share.alternate.url,
            'description':share.description, 
        }
        facebook_api.stream.publish(**{
            'attachment':attachment,
            'uid':str(facebook_id),    
        })
