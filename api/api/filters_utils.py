""" 
Functions that generate Elasticsearch query dictionaries.
"""

group_mapping = {
    'confeitaria': 'Bolos e tortas doces',
    'lanches': 'Lanches',
    'massas': 'Massas',
    'acompanhamentos': 'Saladas, molhos e acompanhamentos',
    'sobremesas': 'Doces e sobremesas',
    'saudavel': 'Alimentação Saudável',
    'carnes': 'Carnes',
    'prato_unico': 'Prato Único',
    'aves': 'Aves',
    'bebidas': 'Bebidas',
    'frutos_do_mar': 'Peixes e frutos do mar',
    'sopas': 'Sopas'
}

class FilterUtils:
    
    def generate_filters(params):
        """
        Returns a dictionary with the filters to be used in the query.
            params: request parameters. Available parameters for filters: 
                    'group', 'time_min', 'time_max', 'portions_min', 
                    'portions_max', 'favorites_min', 'favorites_max'.
        """
        filters = {}
        if 'group' in params:

            if params['group'].isupper():
                raise Exception("Group string should be lowercase")

            filters['group'] = [
                group_mapping[group] 
                for group in params['group'].split(',')
            ]
        
        if 'time_min' in params or 'time_max' in params:
            if 'time_min' in params:
                if not isinstance(params['time_min'], int):
                    raise Exception("time_min isn't numeric")
                if params['time_min'] < 0:
                    raise Exception("time_min is negative")
            if 'time_max' in params:
                if not isinstance(params['time_max'], int):
                    raise Exception("time_max isn't numeric")
                if params['time_max'] < 0:
                    raise Exception("time_max is negative")
            if 'time_min' in params and 'time_max' in params:
                if params['time_min'] > params['time_max']:
                    raise Exception("time_min is bigger than time_max")
            filters['preparation_time'] = (
                params['time_min'] if 'time_min' in params else 0,
                params['time_max'] if 'time_max' in params else 10000000
            )
        
        if 'portions_min' in params or 'portions_max' in params:
            if 'portions_min' in params:
                if not isinstance(params['portions_min'], int):
                    raise Exception("portions_min isn't numeric")
                if params['portions_min'] < 0:
                    raise Exception("portions_min is negative")
            if 'portions_max' in params:
                if not isinstance(params['portions_max'], int):
                    raise Exception("portions_max isn't numeric")
                if params['portions_max'] < 0:
                    raise Exception("portions_max is negative")
            if 'portions_min' in params and 'portions_max' in params:
                if params['portions_min'] > params['portions_max']:
                    raise Exception("portions_min is bigger than portions_max")
            filters['portions'] = (
                params['portions_min'] if 'portions_min' in params else 0,
                params['portions_max'] if 'portions_max' in params else 10000000
            )
        
        if 'favorites_min' in params or 'favorites_max' in params:
            if 'favorites_min' in params:
                if not isinstance(params['favorites_min'], int):
                    raise Exception("favorites_min isn't numeric")
                if params['favorites_min'] < 0:
                    raise Exception("favorites_min is negative")
            if 'favorites_max' in params:
                if not isinstance(params['favorites_max'], int):
                    raise Exception("favorites_max isn't numeric")
                if params['favorites_max'] < 0:
                    raise Exception("favorites_max is negative")
            if 'favorites_min' in params and 'favorites_max' in params:
                if params['favorites_min'] > params['favorites_max']:
                    raise Exception("favorites_min is bigger than favorites_max")
            filters['favorites'] = (
                params['favorites_min'] if 'favorites_min' in params else 0,
                params['favorites_max'] if 'favorites_max' in params else 10000000
            )
        
        if len(filters) == 0:
            return None
        return filters


    def get_filter_queries(filters):
        """
        Returns a list of query dictionaries for filtering.
            filters: dictionary with the following structure:
                {
                    "<range_fild_name>": (start, end),
                    "<multiple_options_field_name>": [option1, option2, ...],
                    ...
                }
        """
        queries = []
        for field_name, field_value in filters.items():
            if isinstance(field_value, tuple):
                queries.append(
                    {
                        "range": {
                            field_name: {
                                "gte": field_value[0],
                                "lte": field_value[1]
                            }
                        }
                    }
                )
            elif isinstance(field_value, list):
                queries.append(
                    {
                        "terms": {
                            field_name+".keyword": field_value
                        }
                    }
                )
        return queries
        

    def get_query_by_name_filtred(name, filters=None, fuzziness=1):
        """
        Returns a query dictionary for searching by name with.
            name: string.
            filters: dictionary with the following structure:
                {
                    "<range_fild_name>": (start, end),
                    "<multiple_options_field_name>": [option1, option2, ...],
                    ...
                }
            fuzziness: int, default 1.
        """
        must = [
            {
                "multi_match": {
                    "query": name,
                    "fields": [
                        "recipe_title^2",
                        "ingredients^2",
                        "raw_text"
                    ],
                    "type": "most_fields",
                    "fuzziness": fuzziness
                }
            }
        ]
        if filters:
            must = must + FilterUtils.get_filter_queries(filters)

        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        return query

    def get_query_by_ingredients_filtred(ingredients, filters=None, fuzziness=1):
        """
        Returns a query dictionary for searching by ingredients with.
            ingredients: list of strings.
            filters: dictionary with the following structure:
                {
                    "<range_fild_name>": (start, end),
                    "<multiple_options_field_name>": [option1, option2, ...],
                    ...
                }
            fuzziness: int, default 1.
        """
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
        if filters:
            must = must + FilterUtils.get_filter_queries(filters)

        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        return query 

    def get_query_by_title_filtred(title, filters=None, fuzziness=1):
        """
        Returns a query dictionary for searching by title with.
            title: string.
            filters: dictionary with the following structure:
                {
                    "<range_fild_name>": (start, end),
                    "<multiple_options_field_name>": [option1, option2, ...],
                    ...
                }
            fuzziness: int, default 1.
        """
        must = [
            {
                "match": {
                    "recipe_title": {
                        "query": title,
                        "fuzziness": 1
                    },
                }
            }
        ]
        if filters:
            must = must + FilterUtils.get_filter_queries(filters)

        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        return query