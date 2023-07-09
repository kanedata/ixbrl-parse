# fmt: off
american_number_system: dict[str, (int | str)]

decimal_words: list[str]


def number_formation(number_words: list[str]) -> int: ...


def get_decimal_sum(decimal_digit_words: list[str]) -> float: ...


def word_to_num(number_sentence: str) -> (int | float | None): ...
