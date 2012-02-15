"""
backends.py -- implements a more universal social api that abstracts away the 
               differences between python social media APIs. The idea is to 
               make server to server interaction uber simple.  Authentication
               is *not* implemented here by design. Use this API once you have
               consumer keys for a user.
               
               Supported networks: Facebook, Twitter, LinkedIn and Debug.
               
               About the debug backend: it writes to stdio. 
               
"""

class ShareError(Exception):
    """Used for social share fails."""
    def __init__(self, msg):
        self.msg=msg
        return

    def __str__(self):
        return "ShareError", self.message or None


# initialize backends
available_backends ={}


def register_share_backend(network, class_name):
    """Registers a new social sharing backend
    
    Parameters:
    network -- name of the social network in lowercase. Something like twitter.
    class_name -- the class that implements the share api"""
    available_backends[network] = class_name

register_share_backend('linkedin','LinkedInBackend')
register_share_backend('twitter','TwitterBackend')
register_share_backend('facebook','FacebookBackend')

class ShareBackend(object):
    """Base class for share backends."""
    
    def __init__(self, api_token, api_secret, consumer_token="", 
                 consumer_secret="", message="", headline="", excerpt="", 
                 tweet="", url="", url_title="", url_description ="", 
                 image_url="", image_url_title="", image_url_description=""):
        """Constructor

        Parameters:
        api_token -- a valid oauth api token. This is your app's token.
        api_secret -- a valid oauth api secret. This is your app's secret.
        consumer_token -- optional consumer token.
        consumer_secret -- optional consumer secret.
        """
        self.api_token = api_token.strip()
        self.api_secret = api_secret.strip()
        self.consumer_token = consumer_token.strip()
        self.consumer_secret = consumer_secret.strip()
        self.to = []
        # deal with message content if we have it
        self.set_content(message, headline=headline, excerpt=excerpt, 
                         tweet=tweet, url=url, url_title=url_title,
                         url_description=url_description, 
                         image_url=image_url, image_url_title=image_url_title,
                         image_url_description=image_url_description)
    
    def set_content(self, message, headline="", excerpt="", tweet="", url="", 
                    url_title="", url_description ="", image_url="", 
                    image_url_title="", image_url_description=""):
        """Sets the content to be shared.  
        
        Parameters:
        message -- the message.
        headline -- the headline or subject for the message
        excerpt -- the excerpt or short version of the message
        tweet -- short 160 character max message
        url -- the url being shared
        url_title -- the title of the url
        url_description -- description of the URL
        image_url -- the url being shared
        image_url_title -- the title of the url
        image_url_description -- description of the URL
        
        """
        self.message = message.strip()
        # truncate at 128 characters
        self.headline = headline[0:128].strip()
        # If there is no excerpt use the headline
        if not hasattr(self, 'excerpt'):
            excerpt = self.headline
        # if there is no tweet defined... create one.
        self.excerpt = excerpt.strip()
        if not hasattr(self, 'tweet'):
            tweet = headline [0:160]
        # truncate tweet if it is too long        
        self.tweet = tweet[0:160].strip()
        self.url = u'%s' % url.strip()
        self.url_title = url_title
        self.url_description = url_description.strip()
        self.image_url = u'%s' % image_url.strip()
        self.image_url_title = image_url_title.strip()
        self.image_url_description = image_url_description.strip()
        
    def share(self):
        """ Executes social network share""" 
        result = self._share()
        return result

    def send_message(self):
        """Sends message using social network. 

        parameters:
        to -- list of recipients in format expected by social network
        """
        # Make sure we have recipients. If not, blow up.
        if self.to == []:
            raise ShareError("No recipients to send to.")
        result = self._send_message()
        return result
        
    def _send_message(self):
        """Sends message: Like the goggles, does nothing."""
        pass

    def _share(self):
        """Shares. Like the goggles, does nothing."""
        pass
    
    
class DebugBackend(ShareBackend):
    """Implements backend for testing. _share and _send_message return message.
    
    you can also set print 
    
    Parameters:
    api_token: a valid oauth api token. This is your app's token.
    api_secret: a valid oauth api secret. This is your app's secret.
    consumer_token: optional consumer token.
    consumer_secret: optional consumer secret.
    
    Backend Specific Parameters:
    print_message: True writes to STDIO. False doesn't print
    """
    
    def __init__(self, *args, **kwargs):
        super(DebugBackend, self).__init__(*args, **kwargs)

    def _share(self, print_message=False):
        """Does social share"""
        if print_message:
            print "consumer token ", self.consumer_token
            print "consumer secret", self.consumer_secret
            print "headline:      ",self.headline
            print "excerpt:       ", self.excerpt or None
            print "message:       ", self.message or None
            print "url:           ", self.url or None
            print "image_url:     ", self.image_url or None
        m = [self.api_token, self.api_secret, self.consumer_secret,
             self.consumer_token, self.headline, self.excerpt, self.message, 
             self.url, self.tweet, self.url_title, self.url_description, 
             self.image_url]
        return m

    def _send_message(self, print_message=False):
        """sends message"""
        if print_message:
            print "consumer token  ", self.consumer_token
            print "consumer secret ", self.consumer_secret
            for t in self.to:
                print "to:        ", t
            print "subject:   ",self.subject
            print "message:   ",self.message or None
            print "url:       ",self.url or None
            print "image_url: ",self.image_url or None        
        m = [self.api_token, self.api_secret, self.consumer_secret,
                     self.consumer_token, self.headline, self.excerpt, self.message, 
                     self.url, self.tweet, self.url_title, self.url_description, 
                     self.image_url,self.to]
        return m        

class LinkedInBackend(ShareBackend):
    """Implements LinedIn Sharing using python-linkedin.

    Backend Settings:
    api_key -- Your API key (get from LinkedIn)
    api_secret -- Your API secret (get from LinkedIn)
    callback_url -- Your callback URL

    LinkedIn Specific Settings:
    visibility -- "connections_only", "anyone" (default) 
    """
    def __init__(self, *args, **kwargs):
        super(LinkedInBackend, self).__init__( *args, **kwargs)
        # Handle custom parameters for backend
        self.callback_url = kwargs.get('callback_url') or ''
        self.visibility = kwargs.get('visibility') or 'anyone'
        # instantiate a linkedin API. 
        from linkedin import linkedin
        # First instantiate the api object.
        self.api = linkedin.LinkedIn(api_key=self.api_token, 
            api_secret=self.api_secret, callback_url='http://localhost.com')
        # Force api to use a stored token/secret instead of getting one.
        # (Due to the way Python-LinkedIN is put together)
        self.api._access_token = self.consumer_token
        self.api._access_token_secret = self.consumer_secret

    def _share(self, connections_only=True):
        """Shares a URL via LinkedIn's API. No web browser required."""
        # set visibility to connections-only or something else...
        if connections_only:
            visibility = 'connections-only'
        else:
            visibility = 'everyone'
            
        result = self.api.share_update(comment=self.message, 
                                       title=self.headline,
                                       submitted_url=self.url, 
                                       submitted_image_url=self.image_url,
                                       description=self.excerpt, 
                                       visibility=visibility)         
        # python-linkedin doesn't do exceptions so we have to check for errors.
        if result == False:
            raise ShareError, self.api.get_error()

    def _send_message(self):
        """Implements python-linkedin send message.

        Note: to is a list of LinkedIn IDs and is truncated at 10 recipients.
        """

        # send the message with LI API
        result = self.api.send_message(subject=self.subject, 
                                       message=self.message, 
                                       ids=self.to)
        # python-linkedin doesn't do exceptions so we have to check for errors.
        if result == False:
            raise ShareError, self.api.get_error()


class TwitterBackend(ShareBackend):
    """Implements Tweepy API 
    
    Backends Settings:
    api_token -- a valid oauth api token. This is your app's token.
    api_secret -- a valid oauth api secret. This is your app's secret.
    consumer_token -- optional consumer token.
    consumer_secret -- optional consumer secret.

    Twitter Specific Settings:
    use_tco -- True or False, use Twitter's t.co shortner.
    """
    def __init__(self, *args, **kwargs):
        super(TwitterBackend, self).__init__(*args, **kwargs)
        # handle twitter custom parameters
        self.use_tco= kwargs.get('use_tco') or True
        # create a tweepy API
        from tweepy import API, OAuthHandler
        auth = OAuthHandler(self.consumer_token, self.consumer_secret)
        auth.set_access_token(self.api_token, self.api_secret)
        # Set up API
        self.api = API(auth)

    def send_message(self, use_tco = 'true'):
        """Processes and sends direct message.
        
        parameters:
        
        use_tco -- use the t.co url shortner
        """
        self.subject = subject.strip()
        self.message = message.strip()
        self.url = url.strip()       
        # Use url t.co url shortner?
        if self.tweet != '':
            self.tweet = _clean_tweet(use_tco=use_tco or False)    
        _send_message()
    
    def _send_message(self):
        """Implemets tweepy send direct message.

        Note: to is a list of Twitter IDs or Twitter usernames.
              Twitter usernames can change, Twitter IDs do not.
        """
        # Loop throught the to's
        from tweepy.error import TweepError
        for t in self.to:
            self.api.send_direct_message(user=t, text=self.tweet)


    def _clean_tweet(self, use_tco=True):
        """Creates tweets by truncating subject at appropriate length.
        
        Length is calculated using the length of a t.co URL or the provided URL
        depending the use_tco parameter. 
        """
        
        if use_tco:
            length = 160 - 19
            tweet = u'%s %s' % self.subject[0:length], self.url
        else:
            length = 160-len(self.url)-1
            tweet = u'%s %s' % self.subject[0:length], self.url
        return tweet

    def _share(self):
        """Implements "sharing" on twitter which is exactly like tweeting.
        
        Note: Tweeting is the same as "updating your status".
        """
        result = self.api.update_status(status=self.tweet)


class FacebookBackend(ShareBackend):
    """Implements Facebook backend"""
    def __init__(self, *args, **kwargs):
        super(FacebookBackend, self).__init__(*args, **kwargs)
        # Create a Facebook social graph API using facepy.     
        from facepy import GraphAPI
        self.api = GraphAPI()
        self.api.oauth_token = self.consumer_token

    def _share(self):
        """Implements sharing on Facebook by making wall posts."""
        # send the message
        # TODO add support for icons to posts and messages
        response = self.api.post(path='me/feed',
                                 message=self.excerpt,
                                 picture=self.image_url or None,
                                 caption = self.image_url_title, 
                                 link = self.url or None,
                                 name=self.url_title,
                                 description=self.url_description)
        if response is None:
            raise ShareError, "Facebook post to feed failed."

    def _send_message(self):
        """Implements send a message to a facebook user"""
        
        # Facebook accepts an array of name/id objects.
        response = self.api.post(path='/me/outbox',
                                 message = self.message,
                                 picture=self.image_url or None,
                                 link = self.url or None,
                                 to=self.to)
        if response is None:
            raise ShareError, "Facebook outbox Failure"


