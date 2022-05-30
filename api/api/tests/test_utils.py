from rest_framework.test import APIClient
from rest_framework import status
#from django.core.urlresolvers import reverse
from django.urls import reverse

from django.test import TestCase

from api.filters_utils import FilterUtils

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def test_generate_filters_no_param(self):
        """Test the generate_filters function with no parameters."""
        params = {}
        filters = None
        self.assertEqual(
            FilterUtils.generate_filters(params),
            filters)
        
    def test_generate_filters_all_params(self):
        """Test the generate_filters function with all parameters."""
        params = {
            'group': 'sopas',
            'time_min': 1,
            'time_max': 2,
            'portions_min': 3,
            'portions_max': 4,
            'favorites_min': 5,
            'favorites_max': 6,
        }
        filters = {
            'group': ['Sopas'],
            'preparation_time': (1, 2),
            'portions': (3, 4),
            'favorites': (5, 6)
        }
        self.assertEqual(
            FilterUtils.generate_filters(params),
            filters)

    def check_if_group_is_lowercase(self):
        params = {
            'group': 'Sopas',
        }
        with self.assertRaisesMessage(Exception,"Group string should be lowercase"):            
            FilterUtils.generate_filters(params) 


    def test_if_time_max_is_bigger_than_time_min(self):
        params = {
            'time_min': 2,
            'time_max': 1,
        }
        with self.assertRaisesMessage(Exception,"time_min is bigger than time_max"):            
            FilterUtils.generate_filters(params) 


    def test_if_portions_max_is_bigger_than_portions_min(self):
        params = {
            'portions_min': 4,
            'portions_max': 3,
        }
        with self.assertRaisesMessage(Exception,"portions_min is bigger than portions_max"):            
            FilterUtils.generate_filters(params) 

    def test_if_favorites_max_is_bigger_than_favorites_min(self):
        params = {
            'favorites_min': 6,
            'favorites_max': 5,
        }
        with self.assertRaisesMessage(Exception,"favorites_min is bigger than favorites_max"):            
            FilterUtils.generate_filters(params) 

    def test_if_time_min_is_numeric(self):
        params = {
            'time_min': 'um',
            'time_max': 2,
        }
        with self.assertRaisesMessage(Exception,"time_min isn't numeric"):            
            FilterUtils.generate_filters(params) 
    
    def test_if_time_max_is_numeric(self):
        params = {
            'time_min': 1,
            'time_max': 'dois',
        }
        with self.assertRaisesMessage(Exception,"time_max isn't numeric"):            
            FilterUtils.generate_filters(params) 

    def test_if_time_min_is_positive(self):
        params = {
            'time_min': -1,
            'time_max': 2,
        }
        with self.assertRaisesMessage(Exception,"time_min is negative"):            
            FilterUtils.generate_filters(params) 

    def test_if_time_max_is_positive(self):
        params = {
            'time_min': 1,
            'time_max': -2,
        }
        with self.assertRaisesMessage(Exception,"time_max is negative"):            
            FilterUtils.generate_filters(params) 

    def test_if_portions_min_is_numeric(self):
        params = {
            'portions_min': 'tres',
            'portions_max': 4,
        }
        with self.assertRaisesMessage(Exception,"portions_min isn't numeric"):            
            FilterUtils.generate_filters(params) 

    def test_if_portions_max_is_numeric(self):
        params = {
            'portions_min': 3,
            'portions_max': 'quatro',
        }
        with self.assertRaisesMessage(Exception,"portions_max isn't numeric"):            
            FilterUtils.generate_filters(params) 

    def test_if_portions_min_is_positive(self):
        params = {
            'portions_min': -3,
            'portions_max': 4,
        }
        with self.assertRaisesMessage(Exception,"portions_min is negative"):            
            FilterUtils.generate_filters(params) 

    def test_if_portions_max_is_positive(self):
        params = {
            'portions_min': 3,
            'portions_max': -4,
        }
        with self.assertRaisesMessage(Exception,"portions_max is negative"):            
            FilterUtils.generate_filters(params) 

    def test_if_favorites_min_is_numeric(self):
        params = {
            'favorites_min': 'cinco',
            'favorites_max': 6,
        }
        with self.assertRaisesMessage(Exception,"favorites_min isn't numeric"):            
            FilterUtils.generate_filters(params) 

    def test_if_favorites_min_is_numeric(self):
        params = {
            'favorites_min': 5,
            'favorites_max': 'seis',
        }
        with self.assertRaisesMessage(Exception,"favorites_max isn't numeric"):            
            FilterUtils.generate_filters(params) 

    def test_if_favorites_min_is_positive(self):
        params = {
            'favorites_min': -5,
            'favorites_max': 6,
        }
        with self.assertRaisesMessage(Exception,"favorites_min is negative"):            
            FilterUtils.generate_filters(params) 

    def test_if_favorites_max_is_positive(self):
        params = {
            'favorites_min': 5,
            'favorites_max': -6,
        }
        with self.assertRaisesMessage(Exception,"favorites_max is negative"):            
            FilterUtils.generate_filters(params) 
        

    def test_get_query_by_name_without_filters(self):
        must = [
            {
                "multi_match": {
                    "query": 'bolo de limão',
                    "fields": [
                        "recipe_title^2",
                        "ingredients^2",
                        "raw_text"
                    ],
                    "type": "most_fields",
                    "fuzziness": 1
                }
            }
        ]
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_name_filtred('bolo de limão', filters=None, fuzziness=1),
                        query)

    def test_get_query_by_name_with_filters(self):
        must = [
            {
                "multi_match": {
                    "query": 'bolo de limão',
                    "fields": [
                        "recipe_title^2",
                        "ingredients^2",
                        "raw_text"
                    ],
                    "type": "most_fields",
                    "fuzziness": 1
                }
            }
        ]
        filters = {
            'group': ['Bolos'],
            'preparation_time': (1, 2),
            'portions': (3, 4),
            'favorites': (5, 6)
        }
        must = must + FilterUtils.get_filter_queries(filters)
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_name_filtred('bolo de limão', filters={
                        'group': ['Bolos'],
                        'preparation_time': (1, 2),
                        'portions': (3, 4),
                        'favorites': (5, 6)
                        }, fuzziness=1),
                            query)

    def test_get_query_by_ingredients_without_filters(self):
        ingredients = ['farinha', 'ovo']
        must = [
            {
                "match": {
                    "ingredients": {
                        "query": ingredient,
                        "fuzziness": 1
                    },
                }
            } for ingredient in ingredients
        ]
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_ingredients_filtred(['farinha', 'ovo'], filters=None, fuzziness=1),
                         query)

    def test_get_query_by_ingredients_with_filters(self):
        ingredients = ['tomate', 'alface']
        must = [
            {
                "match": {
                    "ingredients": {
                        "query": ingredient,
                        "fuzziness": 1
                    },
                }
            } for ingredient in ingredients
        ]
        filters = {
            'group': ['Saladas'],
            'preparation_time': (1, 2),
            'portions': (3, 4),
            'favorites': (5, 6)
        }
        must = must + FilterUtils.get_filter_queries(filters)
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_ingredients_filtred(['tomate', 'alface'], filters={
                        'group': ['Saladas'],
                        'preparation_time': (1, 2),
                        'portions': (3, 4),
                        'favorites': (5, 6)
                        }, fuzziness=1),
                        query)

    def test_get_query_by_title_without_filters(self):
        must = [
            {
                "match": {
                    "recipe_title": {
                        "query": 'salada de atum',
                        "fuzziness": 1
                    },
                }
            }
        ]
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_title_filtred('salada de atum', filters=None, fuzziness=1),
                         query)

    def test_get_query_by_title_with_filters(self):
        must = [
            {
                "match": {
                    "recipe_title": {
                        "query": 'salada de atum',
                        "fuzziness": 1
                    },
                }
            }
        ]
        filters = {
            'group': ['Saladas'],
            'preparation_time': (1, 2),
            'portions': (3, 4),
            'favorites': (5, 6)
        }
        must = must + FilterUtils.get_filter_queries(filters)
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_title_filtred('salada de atum', filters={
                        'group': ['Saladas'],
                        'preparation_time': (1, 2),
                        'portions': (3, 4),
                        'favorites': (5, 6)
                        }, fuzziness=1),
                         query)