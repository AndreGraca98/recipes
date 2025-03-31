import re


def normalize_str(s: str) -> str:
    no_number_string = re.sub(r"\d+", "", s.casefold())
    no_punc_string = re.sub(r"[^\w\s]", "", no_number_string)
    return no_punc_string.strip()
