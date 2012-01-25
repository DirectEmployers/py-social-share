from backends import register_share_backend, DebugBackend, backends
import unittest2

class Tests(unittest2.TestCase):
    def setUp(self):
        self.message = "Corgis are the new cats. Learn to love it."
        self.excerpt = "Corgis have displaced cats on the internet."
        self.title = "Corgis are the new cats."
        self.headline = "Corgis are the new cats. Deal with it.
        self.tweet = 'Corgis = cats. Get over it.'
        self.url = "http://bit.ly/x0c2e8"  # lgt corgis are the new cats
        self.url_title = "Corgis are the New Cats of Internet Culture"
        self.url_description = "According to GeekOut, corgis are the new cats."
        self.image_url = "http://mrg.bz/oDTL0z"
        self.image_url_title = "Laughing Corgi is Laughing"
        self.image_url_description = "lolcorgis > lolcats"
        self.to = ['1','2','3']

    def test_register_share_backend(self):
        """Register backend can register a backend"""
        register_share_backend('test','TestBackend')
        self.assertEqual(backends['test'], 'TestBackend')
        
    def test_debugbackend(self):
        """Tests that the debug backend works."""
        api = DebugBackend (api_token="token", api_secret="shh",
                            consumer_token = "ct", consumer_secret="hush",
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
        self.assertIn(self.api_token ,result)
        self.assertIn(self.api_secret,result)
        self.assertIn(self.consumer_token,result)        
        self.assertIn(self.consumer_secret,result)        
        self.assertIn(self.headline,result)        
        self.assertIn(self.excerpt,result)        
        self.assertIn(self.tweet,result)


if __name__ == '__main__':
    unittest.main()
        