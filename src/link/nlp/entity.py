from elasticsearch import Elasticsearch


def generate_candidates(mention):
    es = Elasticsearch()

    query = {
        'from': 0,
        'size': 100,
        'query': {
            'match': {
                'label': {
                    'query': mention,
                    'operator': 'and',
                }
            }
        }
    }

    res = es.search(index='dictionary', doc_type='entity', body=query)

    candidates = list(map(lambda hit: hit['_source']['id'], res['hits']['hits']))

    return candidates
