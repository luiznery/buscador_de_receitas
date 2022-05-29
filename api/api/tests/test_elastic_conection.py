from django.test import TestCase
from api.elastic_queries import ElasticSearchQueries

class ElasticConectionTestCase(TestCase):
    def test_conection(self):
        elastic_queries = ElasticSearchQueries()
        self.assertTrue('Ping:',elastic_queries.es.ping())