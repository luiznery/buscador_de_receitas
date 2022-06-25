from unittest import skip
from django.test import TestCase
from django.test import Client
import json

@skip('Integration test')
class SearchesTestCase(TestCase):
    def setUp(self):
       self.client = Client()

    def test_search_ingredient(self):
        response=self.client.get('/recipes/search/?ingredients=ovo')
        documents = json.loads(response.content)
        self.assertGreater(len(documents),0)
        for line in documents:
            self.assertIn('ovo',line['raw_text'])

    def test_search_name(self):
        response=self.client.get('/recipes/search/?name=bolo')
        documents = json.loads(response.content)
        self.assertGreater(len(documents),0)
        for line in documents:
            self.assertIn('bolo',line['raw_text'])