from ..providers import Provider, SharingProviderException
from dolt.apis.bitly import Bitly as BitlyAPI
from django.conf import settings

class BitlyProvider(Provider):
    def fulfill(self, alternate):
        bitly_api = BitlyAPI(login=settings.BITLY_LOGIN, apiKey=settings.BITLY_API_KEY)
        url = alternate.original_url.url
        results = bitly_api.shorten(longUrl=url)
        shortened_url = None 
        if results['statusCode'] != 'ERROR':
            shortened_url = results.get('results', {}).get(url, {}).get('shortUrl', None)
        alternate.url = shortened_url
        alternate.save()
        return alternate
