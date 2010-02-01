from d51.django.auth.decorators import auth_required
from django.contrib.sites.models import Site
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ImproperlyConfigured
from .services import load_service, SharingServiceInvalidForm
from .models import URL

SHARE_KEY='u'

@auth_required()
def share_url(request, service_name):
    response = HttpResponseRedirect(request.GET.get('next', '/'))
    url_to_share = request.GET.get(SHARE_KEY, None)
    if url_to_share is None:
        raise Http404
    else:
        full_url_to_share = 'http://%s%s' % ((Site.objects.get_current().domain, url_to_share))
        url, created = URL.objects.get_or_create(
                url=full_url_to_share,
        )
        try:
            url.send(service_name, request.user, request.POST)
        except SharingServiceInvalidForm:
            service = load_service(service_name, url)
            input = [] if request.method != 'POST' else [request.POST]
            form = service.get_form_class()(*input)
            templates, context = [ 
                'sharing/%s/prompt.html'%service_name,
                'sharing/prompt.html' 
            ],{ 
                'service_name':service_name,
                'form': form,
                'url':url_to_share,
                'SHARE_KEY':SHARE_KEY,
                'next':request.GET.get('next','/')
            }
            response = render_to_response(templates, context, context_instance=RequestContext(request))
        except ImproperlyConfigured:
            raise Http404
    return response
