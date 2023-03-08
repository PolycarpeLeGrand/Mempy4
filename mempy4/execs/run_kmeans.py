from mempy4.config import LDA_PATH, KMEANS_PATH, RND_SEED

from mempyapi.ldatopics import LdaModel

from sklearn.cluster import MiniBatchKMeans
from collections import Counter
import pandas as pd


def kmeans_main():
    doc_topics_df = pd.read_pickle(LDA_PATH / 'lda_doc_topics_df.p')
    #clusters = MiniBatchKMeans(n_clusters=7, random_state=RND_SEED).fit_predict(doc_topics_df)
    k = MiniBatchKMeans(n_clusters=7, random_state=RND_SEED).fit(doc_topics_df)

    clusters = k.predict(doc_topics_df)
    distances = k.transform(doc_topics_df)

    print(clusters)
    print(distances)

    return
    doc_cluster_series = pd.Series(index=doc_topics_df.index, data=clusters)

    doc_cluster_series = doc_cluster_series.map(lambda x: f'cluster_{x}')

    doc_cluster_series.to_pickle(KMEANS_PATH / 'doc_cluster_series.p')
    print(doc_cluster_series)
    print(doc_cluster_series[doc_cluster_series == 'cluster_0'])


if __name__ == '__main__':
    kmeans_main()

