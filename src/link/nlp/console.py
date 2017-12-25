import sys

from elasticsearch import Elasticsearch
import spacy
from spacy import displacy


def main():
    es = Elasticsearch()
    nlp = spacy.load('nl')
    doc = nlp(sys.argv[1])

    for ent in doc.ents:
        print(ent.text, ent.label_)

        query = {
            'query': {
                'match': {
                    'label': {
                        'query': ent.text,
                        'operator': 'and',
                    }
                }
            }
        }
        res = es.search(index='dictionary', doc_type='entity', body=query)
        ids = map(lambda hit: hit['_source']['id'], res['hits']['hits'])
        print('%s of %s hits:' % (len(res['hits']['hits']), res['hits']['total']))
        print(''.join(map(lambda id: '  - https://nl.wikipedia.org/wiki/%s\n' % (id), ids)))


if __name__ == '__main__':
    main()
