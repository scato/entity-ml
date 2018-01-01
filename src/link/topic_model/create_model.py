import sys

from gensim import corpora, models, similarities

from link.utils import enable_logging


def main():
    if len(sys.argv) < 5:
        print(
            'Usage: python -m link.topic_model.create_model' + \
            ' <CORPUS> <DICTIONARY> <LSI> <INDEX>'
        )
        exit(1)

    enable_logging()

    # load corpus and dictionary
    corpus = corpora.MmCorpus(sys.argv[1])
    dictionary = corpora.Dictionary.load(sys.argv[2])

    # train model
    lsi = models.LsiModel(
        corpus,
        num_topics=500,
        id2word=dictionary,
        chunksize=20000,
        distributed=False
    )
    lsi.save(sys.argv[3])

    # create similarity matrix
    index = similarities.MatrixSimilarity(lsi[corpus], num_features=500)
    index.save(sys.argv[4])


if __name__ == '__main__':
    main()
