"""Tools to run through saved DocModels and update specific attributes"""

from mempy4.config import DOCMODEL_PATHS_LIST, DOCMODELS_PATH, DOCTYPE_CATS_CSV_PATH, SECONDARY_SUBJECTS_CSV_PATH
from mempy4.utils.generators import generate_docmodels_from_paths
from mempy4.docmodel import DocModel
from mempy4.utils.csvmappings import make_value_mapping_from_csv_path, make_list_mapping_from_csv_path


def update_dm_metadata(doc_id):
    dm = DocModel.read_pickle(DOCMODELS_PATH / f'{doc_id}.p')
    dm.extract_all_metadata()
    dm.extract_citation()
    dm.to_pickle()


def update_dms(*args):
    """Runs the passed functions (without args) on all dms and saves them.

    Function names should be passed as strings
    Usage example: update_dms('update_all_metadata')
    """

    generator = generate_docmodels_from_paths(DOCMODEL_PATHS_LIST)

    for dm in generator:
        for fct in args:
            getattr(dm, fct)()
        dm.to_pickle()


def update_dms_with_mapping(fct, mapping):
    """Updates doctype cat on all dms using the csv mapping specified in config.

    Requires doctypes to be extracted first.
    """

    generator = generate_docmodels_from_paths(DOCMODEL_PATHS_LIST)
    for dm in generator:
        getattr(dm, fct)(mapping)
        dm.to_pickle()


def update_doctype_cats():
    cats = make_value_mapping_from_csv_path(DOCTYPE_CATS_CSV_PATH)
    update_dms_with_mapping('extract_doctype_cat', cats)


def update_secondary_subjects():
    m = make_list_mapping_from_csv_path(SECONDARY_SUBJECTS_CSV_PATH)
    update_dms_with_mapping('extract_secondary_subjects', m)


if __name__ == '__main__':
    # d = '1297-9686-43-25'
    # d = '1471-2105-5-136'
    # d = '1477-9560-7-11'
    # update_dm_metadata(d)

    update_dms('extract_doi')
    # update_doctype_cats()
    # update_secondary_subjects()


