import os
import sys

from gensim import corpora


def main():
    dictionary = corpora.Dictionary.load(os.environ['DICTIONARY'])
    corpus = corpora.MmCorpus(os.environ['CORPUS'])

    token_id = dictionary.token2id[sys.argv[1]]
    doc = corpus[token_id]

    for i, x in doc:
        print(dictionary[i], x)


if __name__ == '__main__':
    main()
