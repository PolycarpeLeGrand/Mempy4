from mempy4.nlpparams import TT_EXCLUDED_TAGS, SPECIAL_CHARACTERS_BASE, TT_NVA_TAGS, SPECIAL_CHARACTERS, TT_VERB_TAGS


def tag_pos_is_word(tag) -> bool:
    return tag.pos not in TT_EXCLUDED_TAGS


def word_has_no_special_char(word: str) -> bool:
    return not any(char in SPECIAL_CHARACTERS for char in word)


def word_has_no_special_char_base(word: str) -> bool:
    return not any(char in SPECIAL_CHARACTERS_BASE for char in word)


def word_is_min_3_chars(word: str) -> bool:
    return len(word) >= 3


def tag_lemma_has_no_special_char(tag) -> bool:
    return word_has_no_special_char(tag.lemma)


def tag_lemma_has_no_special_char_base(tag) -> bool:
    return word_has_no_special_char_base(tag.lemma)


def tag_pos_in_nva(tag) -> bool:
    return tag.pos in TT_NVA_TAGS


def tag_pos_is_verb(tag) -> bool:
    return tag.pos in TT_VERB_TAGS


if __name__ == '__main__':
    pass

