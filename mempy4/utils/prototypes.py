import pandas as pd

from mempy4.config import LDA_OLD_PATH


def old_lda_tests():
    dt = pd.read_pickle(LDA_OLD_PATH / 'doc_topics_df.p')
    tq = pd.read_pickle(LDA_OLD_PATH / 'topic_words_df.p')

    print(dt)
    print(tq)

    return


if __name__ == '__main__':
    old_lda_tests()