from typing import Union
from pathlib import Path
import pandas as pd
import pickle
import json

from mempy4.config import TOPIC_MAPPING, RESULTS_PATH, LEXCOUNTS_PATH, LEXICON_CSV_PATH, COOCS_PATH, TAGCOUNTERS_PATH, SECONDARY_SUBJECTS_CSV_PATH, LDA_PATH
from mempy4.utils.csvmappings import make_list_mapping_from_csv_path
from mempy4.nlpparams import SPECIAL_CHARACTERS_BASE, SPECIAL_CHARACTERS, TT_NVA_TAGS

from mempyapi.lexcats import LexCounter
from mempyapi.coocs import CoocsCounter
from mempyapi.tagcounts import TagCounter

# DFs
# metadata
# journal subjects
# topic-words
# doc-topics
# topic reductions
# cluster
# word occs / corr
# cooc
# cooc refs

# CSVs
# lexicon / lexcats
# doctype cats


def export(target: Union[str, Path], load_ok: bool = True):
    """Export results data to specified folder for use in visualisation project"""

    pass


def export_topic_names_mapping_dict(file_name: str = 'topic_names_mapping_dict.p'):
    """Exports topic the TOPIC_MAPPING {'topic_0': 'Topic Name'} dict defined in config.py

    Saves the dict as a pickle in RESULTS_PATH, file name can be passed as param
    TODO: Change to json
    """

    pickle.dump(TOPIC_MAPPING, open(RESULTS_PATH / file_name, 'wb'))


def export_lexicon_dict(file_name: str = 'lexicon_dict.p'):
    """Exports the lexicon mapping created from the csv at LEXICON_CSV_PATH as a pickled dict

    Dict is structured as {'lex_word': ['word_0', 'word_1']}
    Saves the dict as a pickle in RESULTS_PATH, file name can be passed as param
    TODO: Change to json
    """

    lex = make_list_mapping_from_csv_path(LEXICON_CSV_PATH)
    pickle.dump(lex, open(RESULTS_PATH / file_name, 'wb'))



# Utils for lex corrs / probs
def get_cluster_occs(cluster):
    pass



def lexcats_para_corrs():
    """Exports the para-para lexcat correlations

    Saves the pickled df as lexcorr_paras_full_df.p
    Normalized on diagonal so corr between a lexcat and itself == 0 instead of 1 to help with visualization
    """

    df = pd.read_pickle(LEXCOUNTS_PATH / 'lex_counts_211019' / 'lex_cat_counts_paras_df.p')

    df = df.corr().applymap(lambda x: 0 if x == 1 else x)
    df.to_pickle(RESULTS_PATH / 'lexcorr_paras_full_df.p')


def lexcat_para_occs():
    pass


def coocs_top_dict():
    """Exports the top 100 coocs for each word of the lexicon, both for the full corpus and for each cluster

    Data is structured as nested dicts
    First level keys are the cluster names ('full_corpus' or 'cluster_X')
    Second level keys are lexicon words
    Third level have 2 keys: 'n_occs' (total occs of the word in cluster) and 'coocs', which is a list of tuples
    representing the top 100 cooccurring words, [('word', n_coocs)...]

    TODO: Change to json
    """
    # Top 100 pour chaque mot de coocs, pour chqeu cluster
    # Sous forme de dict {cluster: {word: {'n_occs': n_occs, 'coocs': [(word, coocs),...]}}}
    d = {}
    clusters = ['full_corpus'] + [f'cluster_{i}' for i in range(7)]
    for cluster in clusters:
        df = pd.read_pickle(COOCS_PATH / 'coocs_211212' / f'coocs_df_{cluster}.p')
        cc = CoocsCounter.read_pickle(COOCS_PATH / 'coocs_211212' / f'coocs_counter_{cluster}.p')
        cd = {}

        for word in df.columns:
            n_occs = cc.word_occs[word]
            top_100 = df[word].nlargest(100).astype(int)
            cd[word] = {'n_occs': n_occs, 'coocs': [t for t in top_100.iteritems()]}
        d[cluster] = cd
        print(f'Done with {cluster}')
        print(f'Added top coocs for {len(cd)} words\n')
    pickle.dump(d, open(RESULTS_PATH / 'coocs_top_dict.p', 'wb'))


def export_cooc_refs():
    """Exports the cooc refs sample paragraphs for each lexicon word

    Saves a json file for each cooc pair as word0_word1.json to RESULTS_PATH/cooc_refs/
    """
    refs = pickle.load(open(COOCS_PATH / 'coocs_211212' / 'coocs_detailed_sample_dict.p', 'rb'))
    reduc = pd.read_pickle(RESULTS_PATH / 'topic_reductions_df.p')
    doctopics = pd.read_pickle(RESULTS_PATH / 'lda_doc_topics_df.p')
    words = sorted(list(set(w for t in refs.keys() for w in t)))
    pickle.dump(words, open(RESULTS_PATH / 'cooc_refs_words_list.p', 'wb'))

    for cooc, refs in refs.items():
        for i, ref in enumerate(refs):
            ref['cluster'] = reduc['cluster'][ref['id']]
            ref['topics'] = list(doctopics.loc[ref['id']].nlargest(3).index)
            ref['rank'] = i
        with open(RESULTS_PATH / 'cooc_refs' / f'{cooc[0]}_{cooc[1]}.json', 'w') as f:
            json.dump(refs, f)
        # pickle.dump(refs, open(RESULTS_PATH / 'cooc_refs' / f'{cooc[0]}_{cooc[1]}.p', 'wb'))


def export_token_dfs():
    """Export vocab dfs for NVA lemmas and words found in at least 1000 docs

    Saves the pickled dfs in RESULTS_PATH as lemmas_nva_words_1000docs_df.p and words_pos_lemmas_1000docs_df.p
    """

    # tc = TagCounter.read_pickle(TAGCOUNTERS_PATH / 'text_lemmas_pos.p')
    # Lemmas NVA and their possible words
    df = pd.read_pickle(TAGCOUNTERS_PATH / 'text_lemmas_df.p')
    df = df[df['presence_counts']>=1000].reset_index().sort_values('index').rename({'index': 'lemma'}, axis=1)
    df.to_pickle(RESULTS_PATH / 'lemmas_nva_words_1000docs_df.p')

    # Words NVA and their possible lemmas
    df = pd.read_pickle(TAGCOUNTERS_PATH / 'text_words_df.p')
    df = df[df['presence_counts'] >= 1000].reset_index().sort_values('index').rename({'index': 'word'}, axis=1)
    df.to_pickle(RESULTS_PATH / 'words_pos_lemmas_1000docs_df.p')


def export_source_categories():
    """Exports a {source: [categories]} dict, mapping each source to one or more categories

    TODO: Change to json
    """

    c = make_list_mapping_from_csv_path(SECONDARY_SUBJECTS_CSV_PATH)
    pickle.dump(c, open(RESULTS_PATH / 'categories_dict.p', 'wb'))


def export_metho_stats():

    d = {}

    with open(LDA_PATH / 'legacy_data' / f'docterm_abs_nva_50.p', 'rb') as f:
        dt = pickle.load(f)
        d['abs_lda_tot_tokens'] = sum(len(v) for v in dt.doc_word_counts.values())
        d['abs_lda_unique_tokens'] = len(dt.unique_words)

    with open(TAGCOUNTERS_PATH / 'vocab_counts' / 'text_lemmas_nva_tagcounter.p', 'rb') as f:
        tc = pickle.load(f)
        d['text_lemmas_nva_tot_tokens'] = sum(v for v in tc.total_counts.values())
        d['text__lemmas_nva_unique_tokens'] = len(tc.total_counts)
        #print(tc.total_counts.keys())

    with open(TAGCOUNTERS_PATH / 'vocab_counts' / 'text_words_pos_all_tagcounter.p', 'rb') as f:
        tc = pickle.load(f)
        d['text_words_all_tot_tokens'] = sum(v for v in tc.total_counts.values())
        d['text_words_all_unique_tokens'] = len(tc.total_counts)
        #print(tc.total_counts.keys())

    print(d)


def test2():
    #lda = pickle.load(open(LDA_PATH / 'lda_model.p', 'rb'))
    #print(lda.docterm_df)

    dt = pickle.load(open(LDA_PATH / 'legacy_data' /f'docterm_abs_nva_50.p', 'rb'))
    print(sum(len(v) for v in dt.doc_word_counts.values()))
    print(len(dt.unique_words))


def test():
    # dt = pickle.load(open(LDA_PATH / 'legacy_data' / 'docterm_abs_nva_50.p', 'rb'))
    # wc = dt.doc_word_counts
    # print(dt.total_updates)
    # print(len(dt.unique_words))
    # totals = [sum(v for v in c.values()) for c in wc.values()]
    # tc = TagCounter.read_pickle(TAGCOUNTERS_PATH / 'text_lemmas_pos.p')
    df = pd.read_pickle(TAGCOUNTERS_PATH / 'text_lemmas_df.p')
    print(df)
    #df = df[df['presence_counts'] < 50]
    df = df[TT_NVA_TAGS]
    df = df.sum(axis=1)
    df = df[df>0]
    print(df)
    # df = df.loc[[i for i in df.index if not any(c in SPECIAL_CHARACTERS for c in i)]]
    print(df.sample(100).index)


if __name__ == '__main__':
    #test2()
    export_metho_stats()

