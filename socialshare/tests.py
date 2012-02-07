from backends import DebugBackend, ShareError
from __init__ import register_share_backend, available_backends, Share
import unittest2

class TestBackends(unittest2.TestCase):
    def setUp(self):
        self.api_token = "token"
        self.api_secret = "smokin"
        self.consumer_token = "ticket"
        self.consumer_secret = "golden"
        self.message = "Corgis are the new cats. Learn to love it."
        self.excerpt = "Corgis have displaced cats on the internet."
        self.title = "Corgis are the new cats."
        self.headline = "Corgis are the new cats. Deal with it."
        self.tweet = 'Corgis = cats. Get over it.'
        self.url = "http://bit.ly/x0c2e8"  # lgt corgis are the new cats
        self.url_title = "Corgis are the New Cats of Internet Culture"
        self.url_description = "According to GeekOut, corgis are the new cats."
        self.image_url = "http://mrg.bz/oDTL0z"
        self.image_url_title = "Laughing Corgi is Laughing"
        self.image_url_description = "lolcorgis > lolcats"
        self.to = ['1','2','3']
        register_share_backend('debug','DebugBackend')

    def test_register_share_backend(self):
        """Register backend can register a backend"""
        register_share_backend('test','TestBackend')
        self.assertEqual(available_backends['test'], 'TestBackend')
        
    def test_debugbackend_share(self):
        """Tests that the debug backend works."""
        api = DebugBackend(self.api_token, 
                            self.api_secret,
                            consumer_token=self.consumer_token, 
                            consumer_secret=self.consumer_secret,
                            headline=self.headline, excerpt=self.excerpt,
                            tweet=self.tweet, url=self.url,
                            url_title=self.url.title, 
                            url_description=self.url_description,
                            image_url=self.image_url,
                            image_url_title=self.url_title,
                            image_url_description=self.image_url_description)
        api.to = self.to
        # Do a share
        result = api.share()
        # Now make sure the results were correct
        self.assertIn(self.api_token, result)
        self.assertIn(self.api_secret, result)
        self.assertIn(self.consumer_token, result)        
        self.assertIn(self.consumer_secret, result)        
        self.assertIn(self.headline, result)        
        self.assertIn(self.excerpt, result)        
        self.assertIn(self.tweet, result)
    
    def test_debugbackend_send_message(self):
        """Tests that send message sends messages."""
        api = DebugBackend(self.api_token, self.api_secret,
                           consumer_token=self.consumer_token, 
                           consumer_secret=self.consumer_secret,
                           headline=self.headline, excerpt=self.excerpt,
                           tweet=self.tweet, url=self.url,
                           url_title=self.url.title, 
                           url_description=self.url_description,
                           image_url=self.image_url,
                           image_url_title=self.url_title,
                           image_url_description=self.image_url_description)
        api.to = self.to
        result = api.send_message()
        self.assertIn(self.api_token, result)
        self.assertIn(self.api_secret, result)
        self.assertIn(self.consumer_token, result)        
        self.assertIn(self.consumer_secret, result)        
        self.assertIn(self.headline, result)        
        self.assertIn(self.excerpt, result)        
        self.assertIn(self.tweet, result)
        self.assertIn(self.to, result)
        
    def test_no_recipients(self):
        """Blow up elegantly if no recipients are supplied."""
        api = DebugBackend(self.api_token, self.api_secret,
                           consumer_token=self.consumer_token, 
                           consumer_secret=self.consumer_secret,
                           headline=self.headline, excerpt=self.excerpt,
                           tweet=self.tweet, url=self.url,
                           url_title=self.url.title, 
                           url_description=self.url_description,
                           image_url=self.image_url,
                           image_url_title=self.url_title,
                           image_url_description=self.image_url_description)
        with self.assertRaises(ShareError) as cm:
            api.send_message()
        self.assertEqual(cm.exception.msg, 'No recipients to send to.')
        
    def test_bulk_share(self):
        """Test bulk share processing"""
        share = Share(self.api_token, self.api_secret,
                      consumer_token=self.consumer_token, 
                      consumer_secret=self.consumer_secret,
                      headline=self.headline, excerpt=self.excerpt,
                      tweet=self.tweet, url=self.url,
                      url_title=self.url.title, 
                      url_description=self.url_description,
                      image_url=self.image_url,
                      image_url_title=self.url_title,
                      image_url_description=self.image_url_description,
                      shares = [{'network':'debug', 'consumer_token':'ticket', 
                                'consumer_secret':'golden'}])
        result = share.do_bulk_share()
        self.assertIn(self.api_token, result)
        self.assertIn(self.api_secret, result)
        self.assertIn(self.consumer_token, result)        
        self.assertIn(self.consumer_secret, result)        
        self.assertIn(self.headline, result)        
        self.assertIn(self.excerpt, result)        
        self.assertIn(self.tweet, result)     

if __name__ == '__main__':
    unittest2.main()
        