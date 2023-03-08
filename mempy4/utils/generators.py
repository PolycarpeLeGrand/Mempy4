import pickle

from mempy4.config import DOCMODEL_PATHS_LIST


def generate_docmodels_from_paths(path_list, vocal=True, filter_fct=None):
    """Base generator, yields DocModels based on a path list pointing to pickled DocModels"""

    i = 0
    for path in path_list:
        with open(path, 'rb') as f:
            try:
                dm = pickle.load(f)
                if (filter_fct is None) or filter_fct(dm):
                    i += 1
                    if vocal and i % 5000 == 0:
                        print(f'Generated {i} docmodels')
                    yield dm
            except EOFError:
                print(f'ERROR! Could not open docmodel at: {path}')




def generate_ids_lemmas(path_list, function_name, flatten=True, dms_filter_fct=None, tags_filter_fct=None):
    """Extends generate_docmodels_from_paths, yields pairs of doc_ids and lemma lists

    For each DocModel, yields the doc id (str) and a list of lemmas (str). The specified function should return a list
    of tags with a 'lemma' attribute. If flatten, paragraphs will be merged. Else, each paragraph will be yielded
    individually, and word_list number will be appended to doc id: '{doc id}_{word_list num}'
    """

    for dm in generate_docmodels_from_paths(path_list, filter_fct=dms_filter_fct):
        if flatten:
            yield dm.get_id(), [tag.lemma for tag in getattr(dm, function_name)(flatten=flatten)
                                if tags_filter_fct is None or tags_filter_fct(tag)]
        else:
            for i, para in enumerate(getattr(dm, function_name)(flatten=flatten)):
                yield f'{dm.get_id()}_{i}', [tag.lemma for tag in para if tags_filter_fct is None or tags_filter_fct(tag)]


def generate_ids_tags(path_list, function_name, flatten=True):
    for dm in generate_docmodels_from_paths(path_list):
        if flatten:
            yield dm.get_id(), getattr(dm, function_name)(flatten=flatten)
        else:
            for i, para in enumerate(getattr(dm, function_name)(flatten=flatten)):
                yield f'{dm.get_id()}_{i}', para


def generate_all_docmodels():
    """Shortcut to generate all docmodels from DOCMODEL_PATHS_LIST"""

    return generate_docmodels_from_paths(DOCMODEL_PATHS_LIST)


def generate_all_ids_sentences_tags():

    return generate_ids_tags(DOCMODEL_PATHS_LIST, 'get_text_sentences_tags', flatten=False)

