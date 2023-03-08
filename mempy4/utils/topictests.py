import pandas as pd
import pickle
from pathlib import Path

from mempyapi.docterm import DocTermCounter
from mempyapi.ldatopics import LdaModel
from mempyapi.tagcounts import TagCounter
from mempy4.utils.generators import generate_ids_tags
from mempy4.config import DOCMODEL_PATHS_LIST, LDA_PATH, RND_SEED, TAGCOUNTERS_PATH, BASE_DATA_PATH
from mempy4.utils.filters import tag_pos_in_nva, word_has_no_special_char, word_is_min_3_chars


if __name__ == '__main__':
    dt = DocTermCounter.read_pickle(LDA_PATH / f'docterm_abs_nva_50.p')
    dt = dt.as_df(log_norm=True)

    new_words = [w for w in dt.columns]
    new_ids = [i for i in dt.index]

    old_dt = pd.read_pickle(BASE_DATA_PATH / 'old_docterm_df.p')
    old_words = [w for w in old_dt.columns]
    old_ids = [i for i in old_dt.index]

    dt = dt.reindex(index=old_dt.index, columns=old_dt.columns)

    pickle.dump(list(old_dt.index), open(LDA_PATH / 'ordered_index.p', 'wb'))
    pickle.dump(list(old_dt.columns), open(LDA_PATH / 'ordered_columns.p', 'wb'))

    print(dt)
    print(old_dt)

    print(f'Number of new words: {len(new_words)}')
    print(f'Number of old words: {len(old_words)}')

    print(f'Dataframes are equal: {dt.equals(old_dt)}')

    print()
    print('Words in new but not in old:')

    for w in new_words:
        if w not in old_words:
            print(w)

    print()
    print('Words in old but not in new:')

    for w in old_words:
        if w not in new_words:
            print(w)

    for d in new_ids:
        if d not in old_ids:
            print(d)

    for col in dt.columns:
        if dt[col].eq(old_dt[col]).sum() != len(dt):
            print(col)


