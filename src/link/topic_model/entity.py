import os

from gensim import corpora, matutils, models, similarities


corpus = corpora.MmCorpus(os.environ['CORPUS'])
dictionary = corpora.Dictionary.load(os.environ['DICTIONARY'])
lsi = models.LsiModel.load(os.environ['LSI'])


def id2lsi_vec(vec_id):
    vec = corpus[vec_id]
    return lsi[vec]

def calculate_best_score(candidate_id, reference_ids):
    # translate candidate to LSI vector
    vec_lsi = id2lsi_vec(candidate_id)

    # determine similarities for each of the references
    scores = [
        matutils.cossim(vec_lsi, id2lsi_vec(reference_id))
        for reference_id in reference_ids
    ]

    return max(scores)


def rank_candidates(candidates, reference_entities):
    if len(reference_entities) == 0:
        return candidates

    reference_ids = [
        dictionary.token2id[token]
        for token in reference_entities
    ]

    eligible_candidates = [
        item
        for item in candidates
        if item in dictionary.token2id
    ]

    ranked_candidates = sorted(
        eligible_candidates,
        key=lambda item: -calculate_best_score(
            dictionary.token2id[item],
            reference_ids
        )
    )

    return ranked_candidates
