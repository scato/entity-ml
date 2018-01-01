import os
from pprint import pprint
import sys

from gensim import corpora, models, similarities

from link.utils import enable_logging


def main():
    enable_logging()

    corpus = corpora.MmCorpus(os.environ['CORPUS'])
    dictionary = corpora.Dictionary.load(os.environ['DICTIONARY'])
    lsi = models.LsiModel.load(os.environ['LSI'])
    index = similarities.MatrixSimilarity.load(os.environ['INDEX'])

    # present topics
    pprint(lsi.print_topics(5))

    # use similarity matrix
    token_id = dictionary.token2id[sys.argv[1]]
    vec = corpus[token_id]
    vec_lsi = lsi[vec]
    sims = index[vec_lsi]
    ordered_sims = sorted(enumerate(sims), key=lambda item: -item[1])[1:21]
    results = [(dictionary[sim[0]], sim[1]) for sim in ordered_sims]
    pprint(results)


if __name__ == '__main__':
    main()
