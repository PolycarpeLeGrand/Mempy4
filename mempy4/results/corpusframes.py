"""Functions to make corpus frames - dataframes with doc ids as index and specific data as columns"""

import pandas as pd

from mempy4.utils.filters import tag_pos_is_word, tag_lemma_has_no_special_char_base
from mempy4.utils.generators import generate_docmodels_from_paths
from mempy4.config import RESULTS_PATH, DOCMODEL_PATHS_LIST, LDA_PATH, KMEANS_PATH, TOPIC_MAPPING

from sklearn.manifold import TSNE
from umap import UMAP


def make_metadata_corpusframe(generator, *args):
    """Base metadata df"""

    return pd.DataFrame.from_records([
        {
            'id': dm.id,
            'title': dm.title,
            'year': dm.year,
            'source': dm.source,
            'issn': dm.issn,
            'doctype': dm.doctype,
            'doctype_cat': dm.doctype_cat,
            'url': dm.url,
            'doi': dm.doi,
            'volume': dm.volume,
            'issue': dm.issue,
            'collab': dm.collab,
            'page': dm.page,
            'citation': dm.citation,
            'abs_tokens': len(dm.get_abs_tags(flatten=True)),
            'text_tokens': len(dm.get_text_tags(flatten=True)),
            'abs_words': len([tag for tag in dm.get_abs_tags(flatten=True)
                               if tag_pos_is_word(tag) and tag_lemma_has_no_special_char_base(tag)]),
            'text_words': len([tag for tag in dm.get_text_tags(flatten=True)
                                if tag_pos_is_word(tag) and tag_lemma_has_no_special_char_base(tag)]),
            'abs_n_paras': len(dm.get_abs_tags(flatten=False)),
            'text_n_paras': len(dm.get_text_tags(flatten=False)),
        }
        for dm in generator], index='id').rename_axis(None)


def make_secondary_subjects_corpusframe(generator, *args):
    """One column for each secondary subject, one row for each doc. T/F if doc's source belongs to each subject."""

    doc_subjects_mapping = {dm.id: dm.secondary_subjects for dm in generator}
    unique_subjects = list({subject for subjects in doc_subjects_mapping.values() for subject in subjects})

    return pd.DataFrame.from_dict({doc_id: [s in subjects for s in unique_subjects]
                                   for doc_id, subjects in doc_subjects_mapping.items()},
                                  columns=unique_subjects, orient='index')


def make_topic_reductions_corpusframe(*args):
    """Main topic, 2d and 3d reductions, cluster

    Loads lda_doc_topics_df.p from lda and doc_cluster_series.p from kmeans
    """

    dt_df = pd.read_pickle(LDA_PATH / 'lda_doc_topics_df.p')

    df = pd.DataFrame(index=dt_df.index)

    df['main_topic'] = dt_df.idxmax(axis=1)

    # main topic name col?
    df['main_topic_name'] = df['main_topic'].map(TOPIC_MAPPING)

    df[['umap_2d_x', 'umap_2d_y']] = UMAP(n_components=2, random_state=211).fit_transform(dt_df)
    df[['umap_3d_x', 'umap_3d_y', 'umap_3d_z']] = UMAP(n_components=3, random_state=211).fit_transform(dt_df)

    df[['tsne_2d_x', 'tsne_2d_y']] = TSNE(n_components=2, random_state=211).fit_transform(dt_df)
    df[['tsne_3d_x', 'tsne_3d_y', 'tsne_3d_z']] = TSNE(n_components=3, random_state=211).fit_transform(dt_df)

    s = pd.read_pickle(KMEANS_PATH / 'doc_cluster_series.p')
    df['cluster'] = s

    return df


def make_clusters_corpusframe(*args):
    """Cluster, Top1000(binary, filtre sur cluster == X and top1000 ou juste la dist et on filtre top 100 ou whatev)
    Ou inclure la distance, encore mieux!
    Could be merged with topic reudctions, one dist col per cluster
    """

    return


def combine_corpusframes_to_memviz_format():

    return


def make_and_save_corpusframe(fct, name):
    generator = generate_docmodels_from_paths(DOCMODEL_PATHS_LIST)
    fct(generator).to_pickle(RESULTS_PATH / name)


if __name__ == '__main__':
    make_and_save_corpusframe(make_metadata_corpusframe, 'metadata_corpusframe.p')
    # make_and_save_corpusframe(make_secondary_subjects_corpusframe, 'secondary_subjects_corpusframe.p')
    # make_and_save_corpusframe(make_topic_reductions_corpusframe, 'topic_reductions_corpusframe.p')

