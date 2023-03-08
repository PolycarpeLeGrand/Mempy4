""" LDA exec file

Should not be run again to avoid changes to the existing model. Any minor change in the base data (including the docterm
matrix' column or row order)will affect the resulting topics, and changing the topic model midway would mess everything up.

This was build to replicate the specific state used in a previous version of the project. Don't change it!
"""

import pandas as pd
import pickle
from pathlib import Path

from mempyapi.docterm import DocTermCounter
from mempyapi.ldatopics import LdaModel
from mempyapi.tagcounts import TagCounter
from mempy4.utils.generators import generate_ids_tags
from mempy4.config import DOCMODEL_PATHS_LIST, LDA_PATH, RND_SEED, TAGCOUNTERS_PATH, BASE_DATA_PATH
from mempy4.utils.filters import tag_pos_in_nva, word_has_no_special_char_base, word_is_min_3_chars


def make_abs_docterm():
    """Builds a docterm matrix from text abstracts to be used in lda topic modeling

    Builds DocTerm model from NVA abstract lemmas.
    Loads a tag counter object at [TAGCOUNTERS_PATH / 'abs_lemmas_nva_tagcounter.p'] to remove words with special
    characters and rare words (found in less than x docs, default 50).
    Applies log normalization on term counts.
    """

    min_word_doc_occs = 50
    max_word_freq = 0.3

    dt = DocTermCounter('lemma')
    for doc_id, tag_list in generate_ids_tags(DOCMODEL_PATHS_LIST, 'get_abs_tags', flatten=True):
        dt.update(doc_id, tag_list, filter_fct=tag_pos_in_nva)

    print(f'Done compiling docterm. Total updates: {dt.total_updates}')
    print(f'Unique words: {len(dt.unique_words)}')
    print(f'Loading tagcounter to filter out words found in less than {min_word_doc_occs} docs...')

    tc = TagCounter.read_pickle(TAGCOUNTERS_PATH / 'abs_lemmas_nva_tagcounter.p')
    tc.filter_values(word_has_no_special_char_base)
    tc.filter_values(word_is_min_3_chars)
    tc_df = tc.as_df()
    print(dt.total_updates)
    tc_df = tc_df[(tc_df['article_counts'] >= min_word_doc_occs) & (tc_df['article_counts'] <= max_word_freq * dt.total_updates)]

    dt.filter_values(lambda x: x in tc_df.index)
    print(f'Done filtering, kept {len(dt.unique_words)} words')
    print('Saving docterm model and df...')

    dt.to_pickle(LDA_PATH / f'docterm_abs_nva_{min_word_doc_occs}.p')
    print(dt.as_df(log_norm=True))
    print('Done!')


def make_lda_model():

    # with DocTermCounter.read_pickle(LDA_PATH / f'docterm_abs_nva_50.p') as dt:
    #     docterm_df = dt.as_df(log_norm=True)
    new_index = pickle.load(open(LDA_PATH / 'ordered_index.p', 'rb'))
    new_columns = pickle.load(open(LDA_PATH / 'ordered_columns.p', 'rb'))
    df = DocTermCounter.read_pickle(LDA_PATH / f'docterm_abs_nva_50.p').as_df(log_norm=True)
    df = df.reindex(index=new_index, columns=new_columns)

    lda = LdaModel(
        model_name='topic_model',
        docterm_df=df,
        n_components=80,
        doc_topic_prior=0.2,  # alpha
        topic_word_prior=0.02,  # beta
        max_iter=100,
        learning_decay=0.9,
        random_state=RND_SEED,
        learning_method='batch'
    )
    lda.fit()
    lda.to_pickle(LDA_PATH / 'lda_model.p')

    doc_topics_df = lda.get_doc_topics_df()
    topic_words_df = lda.get_topic_words_df()

    csv = lda.get_word_weights_csv()
    with open(LDA_PATH / 'topic_word_probs.csv', 'wb') as f:
        f.write(csv.encode('utf-8'))

    print(doc_topics_df)
    print(topic_words_df)


def load_lda_make_dfs(lda_path):
    lda = LdaModel.read_pickle(lda_path)

    lda.get_topic_words_df().to_pickle(LDA_PATH / 'lda_topic_words_df.p')
    lda.get_doc_topics_df().to_pickle(LDA_PATH / 'lda_doc_topics_df.p')


if __name__ == '__main__':
    pass
    # make_abs_docterm()
    # make_lda_model()
    # load_lda_make_dfs(lda_path=LDA_PATH / 'lda_model.p')


    # lda = LdaModel.read_pickle(LDA_PATH / 'lda_model.p')
    # csv = lda.get_word_weights_csv()
    # with open(LDA_PATH / 'topic_word_probs.csv', 'wb') as f:
    #     f.write(csv.encode('utf-8'))



