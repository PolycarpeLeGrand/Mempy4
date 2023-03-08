

from mempy4.config import COOCS_PATH
from mempy4.utils.generators import generate_all_ids_sentences_tags
from mempy4.utils.filters import tag_pos_is_verb
from mempyapi.extensions.coocstags import CoocsCounterTags


def make_varb_coocs():
    window = 5
    vocab = ['model', 'mechanism', 'explanation', 'prediction', 'data', 'datum', 'theory', 'study', 'research', 'result', 'role', 'function', 'process', 'cause', 'effect']

    cc = CoocsCounterTags(vocab, window, tag_pos_is_verb)

    for s_id, s in generate_all_ids_sentences_tags():
        cc.update(s_id, s)

    cc.to_pickle(COOCS_PATH / 'verbs_coocs.p')
    df = cc.as_df()
    print(df)
    for word in vocab:
        print(df[word].nlargest(15))


if __name__ == '__main__':
    # make_varb_coocs()

    vocab = ['model', 'mechanism', 'explanation', 'prediction', 'data', 'datum', 'theory', 'study', 'research', 'result', 'role', 'function', 'process', 'cause', 'effect']
    cc = CoocsCounterTags.read_pickle(COOCS_PATH / 'verbs_coocs.p')
    df = cc.as_df()
    print(df)
    for word in vocab:
        print((df[word] / cc.word_occs[word]).nlargest(15))

