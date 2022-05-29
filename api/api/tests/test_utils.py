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

    def check_if_first_letter_is_capslock(self):
        params = {
            'group': 'Sopas',
        }
        # self.assertEqual(FilterUtils.generate_filters(params),
        #                 True)


    def test_if_time_max_is_bigger_than_time_min(self):
        params = {
            'time_min': 2,
            'time_max': 1,
        }
        # self.assertEqual(FilterUtils.generate_filters(params), 
        #                 True)

    def test_if_portions_max_is_bigger_than_portions_min(self):
        params = {
            'portions_min': 4,
            'portions_max': 3,
        }
        # self.assertEqual(FilterUtils.generate_filters(params),
        #                  True)

    def test_if_favorites_max_is_bigger_than_favorites_min(self):
        params = {
            'favorites_min': 6,
            'favorites_max': 5,
        }
        # self.assertEqual(FilterUtils.generate_filters(params), 
        #                 True)

    def test_if_time_is_numeric(self):
        params = {
            'favorites_min': 'um',
            'favorites_max': 2,
        }
        # self.assertEqual(FilterUtils.generate_filters(params), 
        #                 True)

    def test_if_time_is_positive(self):
        params = {
            'favorites_min': 1,
            'favorites_max': -2,
        }
        # self.assertEqual(FilterUtils.generate_filters(params), 
        #                 True)

    def test_if_portions_is_numeric(self):
        params = {
            'portions_min': 'tres',
            'portions_max': 4,
        }
        # self.assertEqual(FilterUtils.generate_filters(params), 
        #                 True)

    def test_if_portions_is_positive(self):
        params = {
            'portions_min': 3,
            'portions_max': -4,
        }
        # self.assertEqual(FilterUtils.generate_filters(params), 
        #                 True)

    def test_if_favorites_is_numeric(self):
        params = {
            'favorites_min': 'cinco',
            'favorites_max': 6,
        }
        # self.assertEqual(FilterUtils.generate_filters(params), 
        #                 True)

    def test_if_favorites_is_positive(self):
        params = {
            'favorites_min': 5,
            'favorites_max': -6,
        }
        # self.assertEqual(FilterUtils.generate_filters(params), 
        #                 True)

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