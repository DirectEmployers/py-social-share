"""
socialshare -- module for sharing to multiple social networks at one time
"""
from backends import *

__version_info__ = {
    'major': 0,
    'minor': 2,
    'micro': 0,
    'releaselevel': 'beta',
    'serial': 1
}

def get_version():
    """
    Return the formatted version information
    """
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)

__version__ = get_version()

class Share(object):                                                                                                                                                               
    """Universal one call shares them all"""                                                                                                                                                                                                                                                                                                                          
    def __init__(self, shares, api_token, api_secret, consumer_token="", 
                 consumer_secret="", message="", headline="", excerpt="", 
                 tweet="", url="", url_title="", url_description ="", 
                 image_url="", image_url_title="", image_url_description=""):
        for share in shares:
            c_t = share['consumer_token'] or consumer_token
            c_s = share['consumer_secret'] or consumer_secret
            class_ = getattr(backends, backends[share['network']], {})
            api = class_(api_token, api_secret, 
                         consumer_token=c_t, consumer_secret=c_s,
                         message=message,
                         headline=headline, 
                         excerpt=excerpt,
                         tweet=tweet, 
                         url=url, url_title=url_title, 
                         url_description=url_description, 
                         image_url=image_url, image_url_title=image_url_title, 
                         image_url_description=image_url_description)
            api.share()
       