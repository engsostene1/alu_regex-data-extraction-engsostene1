# Regex Data Extraction

A Python tool that uses regular expressions to pull structured data out of large blocks of raw text, such as the string responses returned by a data-aggregation API.

Built for the ALU Junior Full Stack Developer regex assignment. All **8** data types are implemented.

## Supported data types

| Data type | Examples that match |
|---|---|
| Email addresses | `user@example.com`, `firstname.lastname@company.co.uk` |
| URLs | `https://www.example.com`, `https://subdomain.example.org/page` |
| Phone numbers | `(123) 456-7890`, `123-456-7890`, `123.456.7890` |
| Credit card numbers | `1234 5678 9012 3456`, `1234-5678-9012-3456` |
| Time (12h and 24h) | `14:30`, `2:30 PM` |
| HTML tags | `<p>`, `<div class="example">`, `<img src="image.jpg" alt="description">` |
| Hashtags | `#example`, `#ThisIsAHashtag` |
| Currency amounts | `$19.99`, `$1,234.56` |

## Project structure

```
.
├── README.md            # this file
├── regex_patterns.py    # all regex patterns, documented, plus compiled PATTERNS dict
├── extractor.py         # extract() and extract_all() helper functions
├── main.py              # demo script: runs extraction on a text file
├── sample_input.txt     # realistic messy input with valid AND invalid data
├── test_patterns.py     # unit tests (valid, invalid and edge cases)
└── .gitignore
```

## Setup

Requires **Python 3.8+**. There are no third-party dependencies (standard library only).

```bash
git clone https://github.com/<your-username>/alu_regex-data-extraction-<your-username>.git
cd alu_regex-data-extraction-<your-username>
python main.py                 # run the demo on sample_input.txt
python main.py my_file.txt     # or run it on your own text file
python -m unittest -v          # run the test suite
```

## Usage in code

```python
from extractor import extract, extract_all

text = "Mail a@b.com, call 123-456-7890, pay $1,234.56 #deal"

extract(text, "emails")        # ['a@b.com']
extract(text, "currency")      # ['$1,234.56']
extract_all(text)              # {'emails': [...], 'urls': [...], ...}
extract("#a #a #b", "hashtags", unique=True)   # ['#a', '#b']
```

## How each pattern works

| Pattern | Explanation |
|---|---|
| **Email** | Local part of letters, digits and `._%+-`, then `@`, then one or more dot-separated domain labels and a TLD of 2+ letters. |
| **URL** | `http`/`https` scheme, dotted hostname, optional port, optional path or query. The last path character cannot be sentence punctuation, so `...page.` does not capture the full stop. |
| **Phone** | Three explicit formats, each with its own consistent separator. Lookarounds stop it matching inside longer digit/hyphen runs (such as a credit card). |
| **Credit card** | Four groups of four digits. A backreference (`\1`) forces the same separator (space or hyphen) between all groups. |
| **Time** | 12-hour: hour 1-12, minutes 00-59, then AM/PM in any case. 24-hour: hour 0-23, minutes 00-59, and not followed by AM/PM, so `13:00 PM` is rejected. |
| **HTML tag** | Opening, closing or self-closing tag with optional attributes (double-quoted, single-quoted or unquoted values). |
| **Hashtag** | `#` followed by word characters with at least one letter or underscore. The lookbehind skips URL fragments (`page#section`) and HTML entities (`&#39;`). |
| **Currency** | `$` then either comma-grouped thousands or plain digits, with an optional 2-digit cents part. |

## Edge cases handled

- **Malformed emails:** `user@`, `@example.com`, `user@.com`, `user@example..com`
- **Invalid URLs:** `www.example.com` (no scheme), `http://` alone, `ftp://` links
- **Phone numbers:** mixed separators (`123-456.7890`) and bad grouping (`123-45-67890`)
- **Credit cards:** mixed separators, 15-digit and 17-digit numbers, no separators
- **Times:** `25:00`, `14:60`, `13:00 PM`; `12:30 PM` is not mis-read as a 24-hour time
- **HTML:** `<>`, `< p>` and maths like `3 < 5 > 2`
- **Hashtags:** a lone `#`, `# space`, `page#section`, `&#39;`, `#123`
- **Currency:** `$1,23.4`, `$.99`, `$19.999`; amounts followed by commas or a full stop still match
- **Multiple matches and formats** in a single string

## Sample output

Running `python main.py` on `sample_input.txt`:

```
Email addresses (3 found)
----------------------------------------
  user@example.com
  firstname.lastname@company.co.uk
  support+billing@mail.example.org

URLs (3 found)
----------------------------------------
  https://www.example.com
  https://subdomain.example.org/page
  https://example.com/search?q=regex&lang=en

Phone numbers (3 found)
----------------------------------------
  (123) 456-7890
  123-456-7890
  123.456.7890

Credit card numbers (2 found)
----------------------------------------
  1234 5678 9012 3456
  1234-5678-9012-3456

Times (5 found)
----------------------------------------
  09:00
  17:45
  12:30 PM
  2:30 PM
  11:15am

HTML tags (10 found)
----------------------------------------
  <html>
  <body>
  <p>
  </p>
  <div class="example">
  </div>
  <img src="image.jpg" alt="description">
  <br/>
  </body>
  </html>

Hashtags (4 found)
----------------------------------------
  #example
  #ThisIsAHashtag
  #regex_2026
  #100DaysOfCode

Currency amounts (4 found)
----------------------------------------
  $19.99
  $1,234.56
  $5
  $1,000,000.00
```

The invalid items deliberately included in `sample_input.txt` (such as `user@`, `123-456.7890`, `25:00` and `$1,23.4`) are correctly ignored.

## Test results

```
$ python -m unittest
...........................
----------------------------------------------------------------------
Ran 27 tests in 0.002s

OK
```

## Known limitations

- Regex cannot fully validate emails (RFC 5322) or parse HTML. These patterns cover the common, realistic formats listed in the assignment.
- Credit card numbers are matched by format only. They are not checked with the Luhn algorithm.
- Currency supports the `$` symbol only.
- A hex colour such as `#fff` looks like a hashtag and will match.

## AI disclaimer

- i have used AI (free plan- Claude) to organise my codes structure and indentations structuring , i have also included some regular expressions from internet .
