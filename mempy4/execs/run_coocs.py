from mempy4.utils.generators import generate_ids_lemmas
from mempy4.utils.timer import Timer
from mempy4.config import COOCS_PATH, DOCMODEL_PATHS_LIST, LEXICON_CSV_PATH, KMEANS_PATH, RND_SEED, DOCMODELS_PATH, MEMVIZ_DATA_PATH
from mempy4.utils.csvmappings import make_list_mapping_from_csv_path
from mempy4.nlpparams import TT_NVA_TAGS
from mempy4.docmodel import DocModel

from mempyapi.coocs import CoocsCounter

from pathlib import Path
from typing import Optional, Callable, Iterable
import pandas as pd
import random
import pickle


WINDOW = 5


def run_coocs_on_ids(doc_ids: Iterable[str], group_name: str, window: int, filter_function: Optional[Callable] = None):
    """Builds, updates and saves a CoocsCounter object for a set of doc ids


    """

    pass


def update_and_save_cc(cc: CoocsCounter, generator: Iterable, working_dir, group_name):
    """Iterates through the generator and updates the CoocCounter. Saves the cc and df"""

    for doc_id, lemmas in generator:
        cc.update(doc_id, lemmas)

    print(f'\n\nDone with {group_name}')

    cc.to_pickle(working_dir / f'coocs_counter_{group_name}.p')
    cc.as_df().to_pickle(working_dir / f'coocs_df_{group_name}.p')


def run_coocs_main():
    """Builds, updates and saves a CoocsCounter object for the full corpus and each cluster.

    Works on full texts, paragraph by paragraph, only NVA tags (generators.generate_ids_lemmas, flatten=False).
    Loads vocab from the lexicon csv (values only, not keys) and calculates cooc values for these words.
    Calls run_coocs_on_ids on each iteration (once on the whole corpus and once per cluster)

    Needs to be able to read clusters from sdads
    """

    print('Running "run_coocs.py" to create and update a new CoocsCounter.')
    exec_name = input('Enter the exec name to proceed (typically YYMMDD): ')
    working_dir = COOCS_PATH / f'coocs_{exec_name}'

    if Path.is_dir(working_dir):
        print('Warning! Path already exists, data might be overwritten!')
    else:
        Path.mkdir(working_dir)

    try:
        lexicon = make_list_mapping_from_csv_path(LEXICON_CSV_PATH)
    except Exception:
        print(f'Error loading lexicon. Make sure the directory contains a valid lexicon CSV.')
        return

    vocab = sorted(list({w for li in lexicon.values() for w in li}))
    print(f'Vocab built, calculating cooc data for {len(vocab)} lemmas')

    cluster_series = pd.read_pickle(KMEANS_PATH / 'doc_cluster_series.p')
    n_clusters = cluster_series.unique()
    print(f'Loaded clusters, running on whole corpus and {len(n_clusters)} clusters')

    print(cluster_series.loc['1471-2121-11-53'])
    execs = [
        {'name': f'cluster_{i}',
         'doc_ids': list(cluster_series[cluster_series == f'cluster_{i}'].index)}
        for i in range(len(n_clusters))
    ]
    execs.append({'name': 'full_corpus', 'doc_ids': list(cluster_series.index)})

    timer = Timer()

    for exec in execs:
        generator = generate_ids_lemmas(DOCMODEL_PATHS_LIST, 'get_text_tags', flatten=False,
                                        dms_filter_fct=lambda x: x.get_id() in exec['doc_ids'],
                                        tags_filter_fct=lambda x: x.pos in TT_NVA_TAGS)

        cc = CoocsCounter(vocab, WINDOW)
        update_and_save_cc(cc, generator, working_dir, exec['name'])

    timer.step('All done!')


def make_ref_from_para_id(pair, para_id):
    doc_id, para_num = para_id.split('_')
    para_num = int(para_num)
    dm = DocModel.read_pickle(DOCMODELS_PATH / f'{doc_id}.p')

    return {
        'id': doc_id,
        'words': pair,
        'para_num': para_num,
        'tot_paras': len(dm.get_raw_text()),
        'title': dm.title,
        'source': dm.source,
        'year': dm.year,
        'citation': dm.citation,
        'para_text': dm.get_raw_text()[para_num],
        'abs_text': dm.get_raw_abs()
    }


def fix_samples_from_cc(base_path, file_name: str = 'coocs_counter_full_corpus.p'):

    # Fix seed to help reproducibility. Will only work if the same values are passed in the same order, e.g. if
    # the lexicon doesnt change between runs. If the lexicon changes, used fix_random_after_lex_change to keep previous
    # order on unchanged values
    random.seed(RND_SEED)
    cc = CoocsCounter.read_pickle(base_path / file_name)

    # Uncomment this (and the part in the loop below) to run only on a subset of coocs containing specific words
    # words = ['mechanism', 'understand', 'explain', 'model', 'theory', 'predict', 'understanding', 'explanation', 'prediction']

    shuffled_ids = {}
    sample_dict = {}

    i = 0
    for pair, counter in cc.refs.items():

        # Use this to only run on pairs containing certain words. Comment out to run on all coocs.
        # if not any(word in pair for word in words):
        #    continue

        para_ids = list(counter.keys())
        random.shuffle(para_ids)
        shuffled_ids[pair] = para_ids

        sample_dict[pair] = [make_ref_from_para_id(pair, para_id) for para_id in para_ids[:20]]
        i += 1
        if i % 1000 == 0:
            print(f'Done with {i} pairs')

    # A dict mapping each cooc tuple to a shuffled list of ids {('mechanism', 'understand'): [id0, id1, ...], ...}
    pickle.dump(shuffled_ids, open(base_path / 'coocs_shuffled_ids_dict.p', 'wb'))

    # A dict mapping each cooc tuple to the result of make_ref_from_para_id for the first 20 shuffled ids
    pickle.dump(sample_dict, open(base_path / 'coocs_detailed_sample_dict.p', 'wb'))

    return


def fix_random_after_lex_change(old_dir_name: str, new_dir_name: str):
    """Loads 21/11/14 cooc ref ids and a newer version, and reorders the shuffled ids based on the old configuration"""

    # NEw ids
    d1 = pickle.load(open(COOCS_PATH / new_dir_name / 'coocs_shuffled_ids_dict.p', 'rb'))

    # Old ids
    d2 = pickle.load(open(COOCS_PATH / old_dir_name / 'shuffled_cooc_refs_dict.p', 'rb'))

    # Samples to update
    r1 = pickle.load(open(COOCS_PATH / new_dir_name / 'coocs_detailed_sample_dict.p', 'rb'))

    for key in d2.keys():
        if key in d1.keys():
            if len(d2[key]) != len(d1[key]):
                print(f'missmatch on {key}')
            else:
                d1[key] = d2[key]
                r1[key] = [make_ref_from_para_id(key, para_id) for para_id in d1[key][:20]]
                if [v.split('_')[0] for v in d1[key][:20]] != [v['id'] for v in r1[key]]:
                    print(f'ops on {key} | {d1[key][:20]} | {[v["id"] for v in r1[key]]}')

    pickle.dump(d1, open(COOCS_PATH / new_dir_name / 'coocs_shuffled_ids_dict.p', 'wb'))
    pickle.dump(r1, open(COOCS_PATH / new_dir_name / 'coocs_detailed_sample_dict.p', 'wb'))


if __name__ == '__main__':
    # run_coocs_main()
    # TODO ATTENTION LE EXEC EST CHANGE POUR JUSTE REFAIRE LE CORPUS COMPLET ET PAS LES CLUSTERS

    # fix_samples_from_cc(COOCS_PATH / 'coocs_211212')
    # fix_random_after_lex_change()

    #sd = pickle.load(open(COOCS_PATH / 'coocs_211212' / 'coocs_detailed_sample_dict.p', 'rb'))
    #words = ['mechanism', 'understand', 'explain', 'model', 'theory', 'predict', 'understanding', 'explanation', 'prediction']
    #d = {k: v for k, v in sd.items() if any(c in words for c in k)}
    #pickle.dump(d, open(MEMVIZ_DATA_PATH / 'cooc_9_refs_sample_dict.p', 'wb'))
    d = pickle.load(open(MEMVIZ_DATA_PATH / 'cooc_9_refs_sample_dict.p', 'rb'))
    print(d[('model', 'understanding')][0].keys())


