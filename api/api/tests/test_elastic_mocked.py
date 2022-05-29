"""Tests.
# """
from django.test import TestCase
from api.elastic_queries import ElasticSearchQueries,parse_result
import mock

import json
search_response = {
    "took" : 12,
    "timed_out" : False,
    "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
    },
    "hits" : {
        "total" : {
        "value" : 8,
        "relation" : "eq"
        },
        "max_score" : 3.3042014,
        "hits" : [
        {
            "_index" : "recipes",
            "_type" : "_doc",
            "_id" : "TzKzRH0ByV2Xbi3OgyAi",
            "_score" : 3.3042014,
            "_source" : {
            "recipe_title" : "Alfaíche",
            "ingredients" : [
                "2 folhas de alface",
                "2 fatias de queijo",
                "1 peito de frango ou salame italiano",
                "1 ovo (opcional)"
            ],
            "group" : "Lanches"
            }
        },
        {
            "_index" : "recipes",
            "_type" : "_doc",
            "_id" : "YDKzRH0ByV2Xbi3OgyAi",
            "_score" : 2.5320065,
            "_source" : {
            "recipe_title" : "Panqueca americana fácil e fofinha",
            "ingredients" : [
                "1 1/2 xícara (chá) de farinha de trigo",
                "1 xícara (chá) de leite",
                "2 colheres (sopa) de manteiga derretida",
                "2 colheres (sopa) de açúcar",
                "1 colher (sopa) de fermento em pó",
                "1 ovo",
                "1 colher (café) de essência de baunilha",
                "1 pitada de sal"
            ],
            "group" : "Lanches"
            }
        },
        {
            "_index" : "recipes",
            "_type" : "_doc",
            "_id" : "PjKzRH0ByV2Xbi3OgyAi",
            "_score" : 2.4872928,
            "_source" : {
            "recipe_title" : "Bolinho de alface",
            "ingredients" : [
                "1 xícara (chá) de alface picada",
                "1 ovo",
                "1 xícara (chá) de farinha de trigo",
                "4 colheres (sopa) de queijo parmesão ralado",
                "2/3 de xícara (chá) de leite",
                "1 colher (chá) de fermento em pó químico",
                "Sal e pimenta-do-reino a gosto",
                "Óleo para fritar"
            ],
            "group" : "Saladas, molhos e acompanhamentos"
            }
        },
        {
            "_index" : "recipes",
            "_type" : "_doc",
            "_id" : "QjKzRH0ByV2Xbi3OgyAi",
            "_score" : 2.4441304,
            "_source" : {
            "recipe_title" : "Pão de mel integral",
            "ingredients" : [
                "4 xícaras de farinha integral",
                "2 xicaras (chá) de especiarias",
                "1 xícara de mel",
                "1 xícara de açúcar mascavo",
                "1 colher (sobremesa) de bicarbonato de sódio",
                "1 ovo",
                "3 colheres de chocolate em pó (opcional)",
                "1/2 xícara de linhaça em pó",
                "1/2 xícara de gérmen de trigo"
            ],
            "group" : "Alimentação Saudável"
            }
        },
        {
            "_index" : "recipes",
            "_type" : "_doc",
            "_id" : "HzKzRH0ByV2Xbi3OgyAi",
            "_score" : 2.3621492,
            "_source" : {
            "recipe_title" : "Bandeclay",
            "ingredients" : [
                "½ xícara de leite morno (120ml)",
                "½ xícara de água morna (120ml)",
                "2 colheres (sopa) de açúcar (25g)",
                "½ colher (sopa) de fermento biológico seco (5g)",
                "1 colher (chá) de leite em pó (4g) (opcional)",
                "2 colheres (sopa) de azeite (30g)",
                "1 ovo médio",
                "½ colher (sopa) de sal (10g)",
                "4 xícaras de farinha de trigo (480g)"
            ],
            "group" : "Lanches"
            }
        },
        {
            "_index" : "recipes",
            "_type" : "_doc",
            "_id" : "ITKzRH0ByV2Xbi3OgyAi",
            "_score" : 2.2136488,
            "_source" : {
            "recipe_title" : "Mini pizza sem glúten com farinha zaya (farinha de mandioca)",
            "ingredients" : [
                "4 rodelas de batata doce cozida amassada (depende da batata, se for pequena, 4 rodelas, se for grossa e grande 1 rodela)",
                "1 ovo",
                "1 colher (sopa) de azeite",
                "3/4 de farinha zaya (farinha de mandioca)",
                "1/2 colher (chá) de sal",
                "1/2 colher (chá) de fermento químico para bolo",
                "3 colheres (sopa) de agua",
                "recheio de acordo com seu gosto"
            ],
            "group" : "Alimentação Saudável"
            }
        },
        {
            "_index" : "recipes",
            "_type" : "_doc",
            "_id" : "GTKzRH0ByV2Xbi3OgyAi",
            "_score" : 2.02289,
            "_source" : {
            "recipe_title" : "Empadas de palmito cremoso",
            "ingredients" : [
                "2 e 1/2 xícaras de farinha de trigo",
                "6 colheres (sopa) de Margarina Claybom gelada",
                "1 ovo (mais 1 gema para pincelar)",
                "3 colheres (sopa) de creme de leite",
                "1/2 colher (chá) de sal",
                "1 colher (sopa) de Margarina Claybom",
                "½ cebola pequena picada",
                "2 xícaras de palmito picado",
                "1 potinho de requeijão",
                "1 colher (chá) de farinha de trigo",
                "½ xícara de azeitona verde sem caroço",
                "sal e pimenta branca a gosto"
            ],
            "group" : "Lanches"
            }
        },
        {
            "_index" : "recipes",
            "_type" : "_doc",
            "_id" : "MTKzRH0ByV2Xbi3OgyAi",
            "_score" : 1.9129901,
            "_source" : {
            "recipe_title" : "Pizza Enrolada",
            "ingredients" : [
                "2 tabletes de fermento biológico",
                "3 colheres (sopa) de açúcar",
                "1 colher (chá) de sal",
                "½ xícara (chá) de óleo de soja",
                "3 xícaras e meia (chá) de farinha de trigo",
                "1 xícara (chá) de água morna",
                "1 embalagem de requeijão",
                "1 embalagem de linguiça fina cortada em rodelas",
                "2 tomates maduros sem pele e sem sementes picados",
                "10 azeitonas pretas picadas",
                "3 ramos de tomilho picados",
                "1 colher (chá) de sal",
                "1 colher (sopa) de azeite",
                "1 gema de ovo batida"
            ],
            "group" : "Massas"
            }
        }
        ]
    }
}


class ElasticSearchQueriesMockedTestCase(TestCase):

    def test_elastic_search_by_name_mocked(self):
        with mock.patch("elasticsearch.Elasticsearch.search") as mocked_search:
            mocked_search.return_value = search_response

            elastic_queries = ElasticSearchQueries()

            recipe = elastic_queries.search_by_name('qualquer coisa mesmo pq ta mocado')

            self.assertEqual(type(recipe),type([]))

    def test_elastic_search_by_title_mocked(self):
        with mock.patch("elasticsearch.Elasticsearch.search") as mocked_search:
            mocked_search.return_value = search_response

            elastic_queries = ElasticSearchQueries()

            recipe = elastic_queries.search_by_title('qualquer coisa mesmo pq ta mocado')

            self.assertEqual(type(recipe),type([]))
    
    def test_elastic_search_by_ingredients_mocked(self):
        with mock.patch("elasticsearch.Elasticsearch.search") as mocked_search:
            mocked_search.return_value = search_response

            elastic_queries = ElasticSearchQueries()

            recipe = elastic_queries.search_by_ingredients('qualquer coisa mesmo pq ta mocado')

            self.assertEqual(type(recipe),type([]))

    def test_elastic_search_by_name_mocked_return_raw(self):
        with mock.patch("elasticsearch.Elasticsearch.search") as mocked_search:
            mocked_search.return_value = search_response

            elastic_queries = ElasticSearchQueries()

            recipe = elastic_queries.search_by_name('qualquer coisa mesmo pq ta mocado',return_raw=True)

            self.assertEqual(type(recipe),type({}))

    def test_elastic_search_by_title_mocked_return_raw(self):
        with mock.patch("elasticsearch.Elasticsearch.search") as mocked_search:
            mocked_search.return_value = search_response

            elastic_queries = ElasticSearchQueries()

            recipe = elastic_queries.search_by_title('qualquer coisa mesmo pq ta mocado',return_raw=True)

            self.assertEqual(type(recipe),type({}))
    
    def test_elastic_search_by_ingredients_mocked_return_raw(self):
        with mock.patch("elasticsearch.Elasticsearch.search") as mocked_search:
            mocked_search.return_value = search_response

            elastic_queries = ElasticSearchQueries()

            recipe = elastic_queries.search_by_ingredients('qualquer coisa mesmo pq ta mocado',return_raw=True)

            self.assertEqual(type(recipe),type({}))
    
    def test_elastic_hostname(self):
        test_host = '333.333.333'
        elastic_queries = ElasticSearchQueries(host=test_host)
        self.assertTrue( test_host in str(elastic_queries.es) )
    
    def test_elastic_port(self):
        test_port = '3333'
        elastic_queries = ElasticSearchQueries(port=test_port)
        self.assertTrue( test_port in str(elastic_queries.es) )
    
    def test_calculate_pagination(self):
        self.assertEqual(calculate_pagination(10,1),0)
        self.assertEqual(calculate_pagination(12,1),0)

        self.assertEqual(calculate_pagination(12,2),12)
        self.assertEqual(calculate_pagination(12,3),24)
    
    def test_parse_result(self):
        result = parse_result(search_response)
        self.assertEqual(result[0]['recipe_title'], search_response['hits']['hits'][0]['_source']['recipe_title'])