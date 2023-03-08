"""Counts the number of occurrences of lexicon words in the documents. Builds and saves LexCounter objects.

1. Make sur the path to the current lexicon file is correctly set in config.py as LEXICON_CSV_PATH
2. Check the EXECS variable below to adjust the exec settings of this script. This is used to specify the data to work
    on (full texts, paragraphs, abstracts, etc) and to map each run to a DocModel function to get that data.
3. Run this script. Enter the exec name when prompted, typically the date as YYMMDD. A 'lex_counts_YYMMDD' dir will be
    created to store the data.
4. A LexCounter (mempyapi.lexcats) will be created and updated for each EXEC entry. Both the LexCounter and a df
    representation with merged categories will be saved in the created dir. The df will have the doc ids as index and
    category names as columns.

tlrd:
To update the lexical counts with a new lexicon, update the lexicon csv and run this. Tadaa!
"""

from mempy4.utils.generators import generate_ids_lemmas
from mempy4.utils.timer import Timer
from mempyapi.lexcats import LexCounter
from mempy4.utils.csvmappings import make_list_mapping_from_csv_path
from mempy4.config import LEXCOUNTS_PATH, DOCMODEL_PATHS_LIST, LEXICON_CSV_PATH

from pathlib import Path

# exec params: name, DocModel getter fct, Flatten paragraphs (count occs on full texts or per paragraph)
EXECS = [
    ('abs', 'get_abs_tags', True),
    ('text', 'get_text_tags', True),
    ('paras', 'get_text_tags', False),
]


def make_and_update_lexcounter(lexicon, generator):
    lc = LexCounter(lexicon)

    for doc_id, word_list in generator:
        lc.update(doc_id, word_list)

    return lc


def calc_and_save_lexcats(dm_paths, base_path, lexicon, name, dm_fct, flatten):

    lc_save_path = base_path / f'lex_counter_{name}.p'

    generator = generate_ids_lemmas(path_list=dm_paths, function_name=dm_fct, flatten=flatten)
    lex_counter = make_and_update_lexcounter(lexicon, generator)

    lex_counter.to_pickle(lc_save_path)
    lex_counter.as_df().to_pickle(base_path / f'lex_cat_counts_{name}_df.p')


def run_lexcats_main():

    print('Running "run_lexcats.py" to create new LexCounters.')
    print(f'This will create {len(EXECS)} new LexCounters: {", ".join(e[0] for e in EXECS)}')
    exec_name = input('Enter the exec name to proceed (typically YYMMDD): ')
    working_dir = LEXCOUNTS_PATH / f'lex_counts_{exec_name}'

    if Path.is_dir(working_dir):
        print('Warning! Path already exists, data might be overwritten!')
    else:
        Path.mkdir(working_dir)

    # load lexicon
    try:
        lexicon = make_list_mapping_from_csv_path(LEXICON_CSV_PATH)
    except Exception:
        print(f'Error loading lexicon. Make sure the directory contains a valid lexicon CSV.')
        return

    # TODO copy lexicon csv in working dir to keep a history

    print('\n\nStarting to process lexcats...')
    timer = Timer()
    for params in EXECS:
        calc_and_save_lexcats(DOCMODEL_PATHS_LIST, working_dir, lexicon, *params)
        timer.step(f'Done with {params[0]}. ')

    print(f'All done!')


def update_lc_ugly():
    """Loads existing lc models and save new cats dfs"""

    lexicon = make_list_mapping_from_csv_path(LEXICON_CSV_PATH)
    path = Path('C:/Users/Sanchez/Desktop/m4data/analysis/lexcats')
    for name in ['abs', 'paras', 'text']:
        lc = LexCounter.read_pickle(path / f'lex_counter_{name}.p')
        lc.lex_mapping = lexicon
        lc._check_lex_mapping()

        lc.as_df().to_pickle(path / 'lex_counts_210924' / f'lex_counts_{name}_df.p')
        print(f'Done with {name}')

    print('done!')


def make_lc_dfs(lc_names, base_path):

    for name in lc_names:
        with base_path / f'lex_counter_{name}.p' as path:
            lc = LexCounter.read_pickle(path)
            lc.as_df().to_pickle(base_path / f'lex_cat_counts_{name}_df.p')


if __name__ == '__main__':
    #run_lexcats_main()
    lc_names = ['text']
    base_path = LEXCOUNTS_PATH / 'lex_counts_211019'
    make_lc_dfs(lc_names, base_path)
    # update_lc_ugly()
