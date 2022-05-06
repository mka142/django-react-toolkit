import os
from django.test import TestCase,Client

from django.conf import settings
from django.contrib.staticfiles import finders

class TestServeReactView(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_serve_indexHtml(self):
        
        with open(settings.REACT_BUILD_DIR /'index.html','rb') as file:
            indexHTML = file.read()

            response = self.client.get('/')

            #files in binary
            self.assertEqual(indexHTML,response.content)
        
    def test_reactStaticFiles(self):
        
        for root,dirs,files in os.walk(settings.REACT_BUILD_DIR / 'static'):
            for name in files:
                result = finders.find(os.path.join(root,name))
                self.assertTrue(result)
        
        
        
        