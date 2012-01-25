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
    """Shares with an arbitrary list of networks and consumer keys. 
    
    Parameters:
    message -- the message.
    headline -- the headline or subject for the message
    excerpt -- the excerpt or short version of the message
    tweet -- short 160 character max message
    url -- the url being shared
    url_title -- the title of the url
    url_description -- description of the URL    
    image_url -- url of picture to share
    image_url_title -- the title fo the image
    image_url_description -- the description of the image
    shares -- list of share networks and keys to share with
              [{'network':'facebook','consumer_token':'token', 
                'consumer_secret':'secret'},...]
    """
    
    def __init__(self, api_token, api_secret, consumer_token="", 
                 consumer_secret="", message="", headline="", excerpt="", 
                 tweet="", url="", url_title="", url_description ="", 
                 image_url="", image_url_title="", image_url_description="",
                 shares=[]):
        # shelf everything for future use
        self.api_token = api_token
        self.api_secret = api_secret
        self.message = message
        self.headline = headline
        self.excerpt = excerpt
        self.tweet = tweet
        self.url = url
        self.url_title = url_title
        self.url_description = url_description
        self.image_url = image_url
        self.image_url_title = image_url_title
        self.image_url_description = image_url_description        
        self.shares = shares
        
    def bulk_share():
        """Shares using all backends in self.shares."""
        for share in self.shares:
            c_t = self.share['consumer_token'] or consumer_token
            c_s = self.share['consumer_secret'] or consumer_secret
            class_ = getattr(backends, backends[share['network']], {})
            api = class_(self.api_token, self.api_secret, 
                         consumer_token=c_t, consumer_secret=c_s,
                         message=self.message,
                         headline=self.headline, 
                         excerpt=self.excerpt,
                         tweet=self.tweet, 
                         url=self.url, url_title=self.url_title, 
                         url_description=self.url_description, 
                         image_url=self.image_url, image_url_title=self.image_url_title, 
                         image_url_description=self.image_url_description)
            api.share()
       
    