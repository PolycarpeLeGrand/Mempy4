
from mempy4.docmodel import DocModel
from mempy4.utils.generators import generate_docmodels_from_paths
from mempy4.config import DOCMODEL_PATHS_LIST, DOCMODELS_PATH, BASE_DATA_PATH

import sys
import pickle
from pathlib import Path


def clone_m3_docmodel(old_dm, save_dir_path):
    new_dm = DocModel(old_dm.origin_file, old_dm.tree, save_dir_path,
                      save_on_init=False, extract_metadata_on_init=False)

    new_dm.year = old_dm.year
    new_dm.title = old_dm.title
    new_dm.source = old_dm.source
    new_dm.doctype = old_dm.doctype
    new_dm.issn = old_dm.issn
    new_dm.keywords = old_dm.keywords
    new_dm.doctype_cat = old_dm.doctype_cat
    new_dm.primary_subjects = old_dm.primary_subjects
    new_dm.secondary_subjects = old_dm.secondary_subjects
    new_dm.raw_text_paragraphs = old_dm.raw_text_paragraphs
    new_dm.raw_abs_paragraphs = old_dm.raw_abs_paragraphs
    new_dm.tt_text_paragraphs = old_dm.tt_text_paragraphs
    new_dm.tt_abs_paragraphs = old_dm.tt_abs_paragraphs

    new_dm.to_pickle()
    return new_dm.file_path


def migrate_dms():
    sys.path.append('C:\\Users\\Sanchez\\Desktop\\Ecole\\Memoire\\Mempy3')
    dm_paths = pickle.load(open(BASE_DATA_PATH / 'id_paths_list.p', 'rb'))
    for dm in generate_docmodels_from_paths(dm_paths):
        clone_m3_docmodel(dm, DOCMODELS_PATH)


def migrate_single_dm(source_dm_path):
    sys.path.append('C:\\Users\\Sanchez\\Desktop\\Ecole\\Memoire\\Mempy3')
    old = pickle.load(open(source_dm_path, 'rb'))
    clone_m3_docmodel(old, DOCMODELS_PATH)


if __name__ == '__main__':
    doc = '1477-9560-7-11.p'
    migrate_single_dm(Path('C:/Users/Sanchez/Desktop/m3data/docmodels') / doc)


