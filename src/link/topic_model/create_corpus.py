from collections import defaultdict
from itertools import islice
from pprint import pprint
import sys

from gensim import corpora, models, matutils
from scipy.sparse import dok_matrix
from tqdm import tqdm

from link.utils import read_object_tuples, get_num_lines, enable_logging


MIN_OUT_DEGREE = 2
MIN_IN_DEGREE = 5


def read_page_links(filename):
    with open(filename, 'r') as fp:
        f = tqdm(fp, total=get_num_lines(filename))
        for object_tuple in read_object_tuples(f):
            yield (object_tuple[0], object_tuple[2])


def read_frequent_page_links(filename):
    page_links = list(read_page_links(filename))

    # remove pages with an in degree of 1
    # and pages with an out degree of less than 5
    out_degree = defaultdict(int)
    in_degree = defaultdict(int)
    for page_link in page_links:
        out_degree[page_link[0]] += 1
        in_degree[page_link[1]] += 1

    return [
        page_link
        for page_link in page_links
        if out_degree[page_link[0]] >= MIN_OUT_DEGREE and in_degree[page_link[1]] >= MIN_IN_DEGREE
    ]


def create_dictionary(filename, page_links):
    dictionary = corpora.Dictionary(page_links, prune_at=None)

    dictionary.save(filename)

    return dictionary


def create_corpus(filename, page_links, dictionary):
    corpus_keys = (
        (
            dictionary.token2id[page_link[1]],
            dictionary.token2id[page_link[0]]
        )
        for page_link in page_links
    )
    corpus_size = max(dictionary.iterkeys()) + 1

    corpus_dok = dok_matrix((corpus_size, corpus_size))
    for corpus_key in corpus_keys:
        corpus_dok[corpus_key] = 1

    corpus_csc = corpus_dok.tocsc()
    corpus = matutils.Sparse2Corpus(corpus_csc)

    # control for DF
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    corpora.MmCorpus.serialize(filename, corpus_tfidf)

    return corpus_tfidf


def main():
    if len(sys.argv) < 4:
        print(
            'Usage: python -m link.topic_model.create_corpus' + \
            ' <PAGE_LINKS> <CORPUS> <DICTIONARY>'
        )
        exit(1)

    enable_logging()

    frequent_page_links = read_frequent_page_links(sys.argv[1])
    dictionary = create_dictionary(sys.argv[3], frequent_page_links)
    corpus = create_corpus(sys.argv[2], frequent_page_links, dictionary)


if __name__ == '__main__':
    main()
