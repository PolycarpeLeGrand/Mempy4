from pathlib import Path
import pandas as pd
import json
import pickle
from mempy4.config import LDA_PATH


save_path = Path('C:/Users/Sanchez/Desktop/Prog/Pycharm Projects/Scientific Explanation/charting/data/legacy')


def export_ids():
    meta_path = Path('C:/Users/Sanchez/Desktop/m4data/memviz/dataframes/metadata_corpusframe.p')
    df = pd.read_pickle(meta_path)
    ids = list(df.index)
    print(f'Total ids: {len(ids)}')
    with open(save_path / 'legacy_ids.json', 'w', encoding='utf-8') as f:
        json.dump(ids, f, ensure_ascii=False, indent=4)


def export_docterm_labels():
    new_index = pickle.load(open(LDA_PATH / 'legacy_data' / 'ordered_index.p', 'rb'))
    new_columns = pickle.load(open(LDA_PATH / 'legacy_data' / 'ordered_columns.p', 'rb'))
    d = {'index': new_index, 'columns': new_columns}
    with open(save_path / 'legacy_docterm_labels.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    #export_ids()
    export_docterm_labels()
