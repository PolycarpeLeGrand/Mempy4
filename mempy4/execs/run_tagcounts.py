

from mempyapi.tagcounts import TagCounter
from mempy4.utils.generators import generate_ids_tags
from mempy4.config import DOCMODEL_PATHS_LIST, TAGCOUNTERS_PATH
from mempy4.nlpparams import TT_NVA_TAGS


def build_tagcount(dm_fct_name, tag_attr='lemma', secondary_attr=None, filter_fct=None, save_name=None):

    print('Building tagcounter...')
    tc = TagCounter(tag_attr, secondary_attr)

    for _, tags in generate_ids_tags(DOCMODEL_PATHS_LIST, dm_fct_name, flatten=True):
        tc.update(tags, filter_fct=filter_fct)

    print(f'Done building tagcounter, total updates: {tc.total_updates}')
    if save_name is not None:
        tc.to_pickle(TAGCOUNTERS_PATH / 'vocab_counts' / save_name)
        print(f'Pickled and saved as {save_name}')
    return tc


if __name__ == '__main__':

    # Text lemmas with pos, no filter
    build_tagcount(
        dm_fct_name='get_text_tags',
        tag_attr='lemma',
        secondary_attr='pos',
        filter_fct=None,
        save_name='text_lemmas_pos_all_tagcounter.p')

    # Text words with pos, no filter
    build_tagcount(
        dm_fct_name='get_text_tags',
        tag_attr='word',
        secondary_attr='pos',
        filter_fct=None,
        save_name='text_words_pos_all_tagcounter.p')

    # Text lemmas, NVA pos only
    build_tagcount(
        dm_fct_name='get_text_tags',
        tag_attr='lemma',
        secondary_attr=None,
        filter_fct=lambda x: x.pos in TT_NVA_TAGS,
        save_name='text_lemmas_nva_tagcounter.p')


