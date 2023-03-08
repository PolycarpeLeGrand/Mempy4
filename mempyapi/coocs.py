"""Coocs!"""

from typing import Callable, Iterable, Optional
from collections import defaultdict, Counter
import pandas as pd
import pickle


class CoocsCounter:
    """Object used to count word cooccurrences across a series of texts.

    Works from a vocabulary list. Counts all words cooccurring with each vocab word, within the specified window.
    Also tracks which combinations of vocab word cooccur at least once in each document, making it easy to retrieve the
    ids of all documents in which any specific combination of vocab words were found in the same cooccurrence.

    Ref tracking might consume a lot of memory on large corpus / vocabularies. Consider updating coocs only if it
    becomes a problem.

    Attributes
    ----------
    vocab: Iterable[str]
        The list of targeted words to count cooccurrences on.
    window: int
        How many words to consider in each direction when counting cooccurrences for a targeted word. The value is
        inclusive.
    coocs: defaultdict[Counter]
        Variable used to track the cooccurrences. Dict mapping each vocab word to a Counter tracking its cooccurring
        terms.
    refs: set[tuple]
        Collection of tuples tracking cooccurrence references.
    word_occs: Counter
        Tracks how many times each vocab word was found.

    """

    def __init__(self, vocab: list[str], window: int):
        """CoocsCounter constructor,

        Parameters
        ----------
        vocab: Iterable[str]
            The list of targeted words to count cooccurrences on.
        window: int
            The cooccurrence window (inclusive).
        """

        self.vocab = vocab
        self.window = window
        self.coocs = defaultdict(Counter)
        self.word_occs = Counter()
        self.pairs = [
            tuple(sorted([w1, w2])) for i, w1 in enumerate(self.vocab) for j, w2 in enumerate(self.vocab[i+1:])
        ]
        # Keys: (word, word) sorted
        # values: para, n coocs for each pair. Counts are doubled since registered both for word1 and word2
        self.refs = defaultdict(Counter)

    def update(self, doc_id: str, word_list: Iterable[str],
               update_coocs: Optional[bool] = True, update_refs: Optional[bool] = True):
        """Updates cooccurrence values and references with passed values.

        If update coocs: For each vocab word in the passed word_list, gets the words within the window and updates the
        counter.
        If update refs: If two or more vocab word are found within the same window, the doc reference will be recorded.

        Parameters
        ----------
        doc_id
            Unique identifier of the document. If working on paragraphs, paragraph number should be appended to doc id
            to make sure each one has a unique id.
        word_list: list-like of str
            List of strings representing the document's words.
        update_coocs: bool
            Whether to update cooccurrence counts
        update_refs: bool
            Whether to update vocab words cooccurrence references
        """

        for i, word in enumerate(word_list):
            if word in self.vocab:
                self.word_occs.update([word])
                beg = max(i - self.window, 0)
                end = i + self.window + 1
                sequence = [w for w in word_list[beg:end] if w != word]

                if update_coocs:
                    self.coocs[word].update(sequence)

                if update_refs:
                    # Update refs if at least 2 vocab words are found
                    # if sum(vals := [w in sequence for w in self.vocab]) >= 2:

                    for cooc in sequence:
                        if cooc in self.vocab:
                            self.refs[tuple(sorted([word, cooc]))].update([doc_id])

    def update_coocs_only(self, doc_id: str, word_list: Iterable[str]):
        """Calls update with coocs only (id, word_list, True, False). Might be cleaner in some cases."""

        self.update(doc_id, word_list, True, False)

    def update_refs_only(self, doc_id: str, word_list: Iterable[str]):
        """Calls update with refs only (id, word_list, False, True). Might be cleaner in some cases."""

        self.update(doc_id, word_list, False, True)

    def as_df(self, filter_fct: Optional[Callable[[str], bool]] = None):
        """Returns a DataFrame with cooccurrence results

        Columns are vocab words (as specified on init) that were found at least once in update texts.
        Index are all words with at least one cooccurrence with a vocab word.
        """

        if filter_fct is not None:
            filtered_cooc_terms = list(filter(filter_fct, {word for counter in self.coocs.values() for word in counter.keys()}))
            return pd.DataFrame(self.coocs, index=filtered_cooc_terms)
        else:
            return pd.DataFrame(self.coocs)

    def to_pickle(self, path):
        """Pickles the LexCounter object at the specified location."""

        pickle.dump(self, open(path, 'wb'))

    @classmethod
    def read_pickle(cls, path):
        return pickle.load(open(path, 'rb'))
