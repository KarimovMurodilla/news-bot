from fuzzywuzzy import fuzz


def calculate(title1: str, title2):
    result = fuzz.ratio(title1, title2)
    return result
