#this file contains regex patterns for extracting various types of data from text,
#such as email addresses, URLs, phone numbers, credit card numbers, times, HTML tags, hashtags, and currency amounts. 
#Each pattern is defined as a raw string (r"") to avoid issues with escape sequences. The patterns are compiled into regex objects and stored in a dictionary called PATTERNS for easy access.
#import re means we are importing the re module, which provides support for regular expressions in Python. We will use this module to compile the regex patterns defined in this file.
import re

# ---------------------------------------------------------------------------
# QUICK REMINDER (so I don't forget what the symbols mean):
#   [abc]   = any ONE of these characters        [^abc] = anything EXCEPT these
#   +       = one or more                        *      = zero or more
#   ?       = optional (zero or one)             {2,}   = two or more
#   \d      = a digit        \w = letter/digit/_        \s = whitespace
#   \b      = word boundary (edge between a word and a non-word)
#   (?: )   = group things together, but don't remember them
#   (?<! )  = "look BEHIND: make sure this does NOT come right before"
#   (?! )   = "look AHEAD: make sure this does NOT come right after"
#   (?= )   = "look AHEAD: make sure this DOES come after"
# The r before each string means "raw": Python leaves my backslashes alone,
# so \d stays \d instead of Python trying to read it as a special character.
# ---------------------------------------------------------------------------


EMAIL = r"\b[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b" #all regex patterns are defined as raw strings (r"") to avoid issues with escape sequences. The EMAIL pattern matches email addresses by looking for a sequence of characters that includes letters, digits, and certain special characters, followed by an "@" symbol, a domain name, and a top-level domain.

URL = (
    r"https?://"       #matches URLs that start with "http://" or "https://"
    r"(?:www\.)?"      #optionally matches "www."
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}"  #matches the domain name, which consists of one or more labels separated by dots. Each label must start and end with an alphanumeric character and can contain hyphens in between. The top-level domain must be at least two characters long.
    r"(?::\d{2,5})?"        #optionally matches a port number, which consists of a colon followed by 2 to 5 digits.
    r"(?:/(?:[^\s<>\"']*[^\s<>\"'.,;:!?)])?)?"    #optionally matches a path, which starts with a forward slash and can contain any characters except whitespace, angle brackets, quotes, and certain punctuation marks. The path cannot end with certain punctuation marks like .,;:!?).
)

PHONE = (
    r"(?<![\w-])"   #this is a negative lookbehind assertion that ensures the phone number is not preceded by a word character (letter, digit, or underscore) or a hyphen. This helps to avoid matching phone numbers that are part of larger words or strings.
    r"(?:\(\d{3}\) ?\d{3}-\d{4}"        #this part of the pattern matches phone numbers in the format (123) 456-7890. It looks for an opening parenthesis, followed by exactly three digits, a closing parenthesis, an optional space, exactly three digits, a hyphen, and exactly four digits.
    r"|\d{3}-\d{3}-\d{4}"        #this part of the pattern matches phone numbers in the format 123-456-7890. It looks for exactly three digits, a hyphen, exactly three digits, another hyphen, and exactly four digits.
    r"|\d{3}\.\d{3}\.\d{4})"     #this part of the pattern matches phone numbers in the format 123.456.7890. It looks for exactly three digits, a period, exactly three digits, another period, and exactly four digits.
    r"(?![\w-])"                 #this is a negative lookahead assertion that ensures the phone number is not followed by a word character (letter, digit, or underscore) or a hyphen. This helps to avoid matching phone numbers that are part of larger words or strings.
)

#this pattern matches credit card numbers in the format 1234-5678-9012-3456 or 1234 5678 9012 3456. It looks for exactly four digits, followed by either a space or a hyphen (captured as group 1), then exactly four digits, the same separator as before (referenced by \1), another four digits, the same separator again, and finally another four digits. The negative lookbehind and lookahead assertions ensure that the credit card number is not part of a larger string of digits or hyphens.
CREDIT_CARD = r"(?<![\d-])\d{4}([ -])\d{4}\1\d{4}\1\d{4}(?![\d-])"   
# 12-hour: 1-12, minutes 00-59, then AM/PM (any case, optional space).
TIME_12H = r"(?<![\d:])(?:0?[1-9]|1[0-2]):[0-5]\d\s?[AaPp][Mm]\b"
# 24-hour: 0-23, minutes 00-59. Not followed by AM/PM, seconds or more digits,
TIME_24H = r"(?<![\d:])(?:[01]?\d|2[0-3]):[0-5]\d(?!\d|:\d|\s?[AaPp][Mm]\b)"
TIME = f"{TIME_12H}|{TIME_24H}"

HTML_TAG = (              #this pattern matches HTML tags, which can be opening or closing tags with optional attributes. It looks for an opening angle bracket, an optional forward slash (for closing tags), a tag name that starts with a letter and can contain letters and digits, followed by zero or more attributes. Each attribute consists of a name (starting with a letter or underscore) and an optional value, which can be enclosed in double quotes, single quotes, or be unquoted. The pattern ends with an optional forward slash (for self-closing tags) and a closing angle bracket.
    r"</?[A-Za-z][A-Za-z0-9]*"
    r"(?:\s+[A-Za-z_:][-\w:.]*"
    r"(?:\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s\"'=<>`]+))?)*"
    r"\s*/?>"
)

HASHTAG = r"(?<![\w&#/])#(?=[A-Za-z0-9_]*[A-Za-z_])[A-Za-z0-9_]+"   #this pattern matches hashtags, which start with a "#" symbol and are followed by a sequence of letters, digits, or underscores. The negative lookbehind assertion ensures that the hashtag is not preceded by a word character, "&", "#", or "/", while the positive lookahead assertion ensures that there is at least one letter or underscore in the hashtag.

#this pattern matches currency amounts in US dollars, which start with a "$" symbol and are followed by a number that can include commas as thousand separators and an optional decimal part with exactly two digits. The negative lookbehind assertion ensures that the currency amount is not preceded by a word character, comma, or period, while the negative lookahead assertion ensures that it is not followed by a digit, comma followed by a digit, or period followed by a digit.
CURRENCY = r"(?<![\w.,])\$(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{2})?(?!\d|,\d|\.\d)"   

#this dictionary compiles all the regex patterns defined above into regex objects using re.compile. Each key in the dictionary corresponds to a data type (e.g., "emails", "urls"), and the value is the compiled regex pattern for that data type. This allows for efficient pattern matching when extracting data from text.
PATTERNS = {
    "emails": re.compile(EMAIL),
    "urls": re.compile(URL),
    "phone_numbers": re.compile(PHONE),
    "credit_cards": re.compile(CREDIT_CARD),
    "times": re.compile(TIME),
    "html_tags": re.compile(HTML_TAG),
    "hashtags": re.compile(HASHTAG),
    "currency": re.compile(CURRENCY),
}
#above pattern dictionary is used in extractor.py to extract matches from a given text using the extract and extract_all functions. Each pattern can be accessed by its corresponding key in the PATTERNS dictionary, allowing for easy extraction of specific data types from text.