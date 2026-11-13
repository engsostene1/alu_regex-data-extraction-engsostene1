#Functions that run the compiled patterns over a block of text.
#we import the compiled patterns from regex_patterns.py and use them to extract matches from a given text. The extract function takes a text string, a kind of data to extract (e.g., "emails"), and an optional unique flag to remove duplicates. The extract_all function runs all patterns on the text and returns a dictionary of matches for each data type.
from regex_patterns import PATTERNS

def extract(text, kind, unique=False):  #this function takes a text string, a kind of data to extract (e.g., "emails"), and an optional unique flag to remove duplicates. It returns a list of matches for the specified kind of data.
   #step1: check if the kind is in the PATTERNS dictionary. If not, raise a KeyError with a message indicating the unknown data type and the available options.
    if kind not in PATTERNS:
        raise KeyError(f"Unknown data type: {kind!r}. Choose from {list(PATTERNS)}")

    #step2: use the compiled regex pattern for the specified kind to find all matches in the text. We use finditer to get an iterator of match objects, and then extract the matched string using group(0). This is necessary because some patterns may contain capture groups, and we want the entire match.    
    # finditer + group(0) because some patterns contain capture groups
    matches = [m.group(0) for m in PATTERNS[kind].finditer(text)]

    #step3: if the unique flag is set to True, remove duplicates while keeping the first-seen order. We use dict.fromkeys to create a dictionary with the matches as keys, which automatically removes duplicates, and then convert it back to a list.
    if unique:
        matches = list(dict.fromkeys(matches))
    return matches

#unique=false by default, meaning that duplicates will be kept unless specified otherwise. The function returns a list of matches for the specified kind of data.
def extract_all(text, unique=False):
    #this function runs all patterns on the text and returns a dictionary of matches for each data type. It takes a text string and an optional unique flag to remove duplicates. The result is a dictionary where the keys are the data types (e.g., "emails") and the values are lists of matches for each type.
    return {kind: extract(text, kind, unique) for kind in PATTERNS}