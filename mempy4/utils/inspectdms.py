import random

from mempy4.config import DOCMODEL_PATHS_LIST, DOCMODELS_PATH, DOCTYPE_CATS_CSV_PATH
from mempy4.utils.generators import generate_docmodels_from_paths
from mempy4.nlpparams import TT_EXCLUDED_TAGS
from mempy4.docmodel import DocModel


def meta_extract_tests(sample_size=15):
    p = random.sample(DOCMODEL_PATHS_LIST, sample_size)
    generator = generate_docmodels_from_paths(p)
    for dm in generator:
        print(f'Doc: {dm.id}')
        dm.extract_all_metadata()
        dm.extract_citation()

        for key, val in dm.__repr__().items():
            print(f'{key}: {val}')
        print(dm.citation)
        print(dm.file_path)
        print('\n')

    # dm = DocModel.read_pickle(DOCMODELS_PATH / '1477-7525-4-46.p')
    # dm.tree.write('t.xml')


def check_len():
    p = random.sample(DOCMODEL_PATHS_LIST, 15)
    generator = generate_docmodels_from_paths(p)
    for dm in generator:
        print(f'Doc: {dm.id}')
        t = dm.get_abs_tags(flatten=True)
        print(len(t))
        print(len([tag for tag in t if tag.pos not in TT_EXCLUDED_TAGS]))


def inspect_dm(doc_id):
    dm = DocModel.read_pickle(DOCMODELS_PATH / f'{doc_id}.p')
    print(dm.__repr__())
    # dm.tree.write('t.xml')


def get_sentences(doc_id):
    dm = DocModel.read_pickle(DOCMODELS_PATH / f'{doc_id}.p')
    for s in dm.get_text_sentences_tags():
        print(s)


if __name__ == '__main__':
    doc = '1477-9560-7-11'
    get_sentences(doc)
