# fmt: off
from typing import Dict, List, Union

american_number_system: Dict[str, Union[int, str]]

decimal_words: List[str]


def number_formation(number_words: List[str]) -> int: ...  # noqa: E704


def get_decimal_sum(decimal_digit_words: List[str]) -> float: ...  # noqa: E704


def word_to_num(number_sentence: str) -> Union[int, float, None]: ...  # noqa: E704
