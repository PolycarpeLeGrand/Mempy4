
from typing import Callable, Iterable, Optional

from mempyapi.coocs import CoocsCounter


class CoocsCounterTags(CoocsCounter):

    def __init__(self, vocab: list[str], window: int,
                 cooc_tag_filter_fct: Callable[[any], bool],
                 tag_attribute: Optional[str] = 'lemma',):

        self.tag_attr = tag_attribute
        self.filter_fct = cooc_tag_filter_fct
        super().__init__(vocab, window)

    def update(self, doc_id: str, tag_list,
               update_coocs: Optional[bool] = True,
               update_refs: Optional[bool] = True):

        for i, tag in enumerate(tag_list):
            if getattr(tag, self.tag_attr) in self.vocab and not self.filter_fct(tag):
                self.word_occs.update([tag.lemma])
                beg = max(i - self.window, 0)
                end = i + self.window + 1
                sequence = tag_list[beg:end]

                if update_coocs:
                    self.coocs[getattr(tag, self.tag_attr)].update([getattr(t, self.tag_attr) for t in sequence if (t.lemma != tag.lemma) and (self.filter_fct(t))])