import sys

import spacy
from spacy import displacy

from link.nlp.entity import generate_candidates
from link.topic_model.entity import rank_candidates


def main():
    nlp = spacy.load('nl')
    doc = nlp(sys.argv[1])

    # fetch candidates by mention
    candidates_by_mention = {}
    for ent in doc.ents:
        if not doc.text in candidates_by_mention:
            candidates_by_mention[ent.text] = generate_candidates(ent.text)

    # order mentions by number of candidates
    candidates_by_mention = dict(sorted(
        candidates_by_mention.items(),
        key=lambda item: len(item[1])
    ))

    reference_entities = []
    for mention, candidates in candidates_by_mention.items():
        print(mention)

        ranked_candidates = rank_candidates(candidates, reference_entities)

        if len(ranked_candidates) > 0:
            reference_entities.append(ranked_candidates[0])

        ranked_candidates = ranked_candidates[:10]
        print(''.join(map(lambda id: '  - https://nl.wikipedia.org/wiki/%s\n' % (id), ranked_candidates)))


if __name__ == '__main__':
    main()
