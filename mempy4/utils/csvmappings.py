import csv


def make_list_mapping_from_csv_path(csv_path):
    """Reads a csv and makes a key: [values] mapping

    Adds one entry per row, using the first column as the key and the rest as a value list. Ignores rows with no value
    in the first column.
    """

    f = open(csv_path, newline='')
    d = {n[0]: [n[i + 1] for i in range(len(n) - 1) if n[i + 1] != ''] for n in csv.reader(f)}

    # Remove categories with no associated value
    d = {cat: words for cat, words in d.items() if len(words) > 0}

    return d


def make_value_mapping_from_csv_path(csv_path):
    """Reads a csv and make a key: value mapping

    For each row, uses the first column as key and the second column as value. Other columns are ignored.
    """

    f = open(csv_path, newline='')
    return {n[0]: n[1] for n in csv.reader(f) if (n[0] != '') and (n[1] != '')}


