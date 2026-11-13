#this is test file used to test valid input , invalid inputs and tricky cases 
import unittest

from extractor import extract, extract_all

class PatternTestCase(unittest.TestCase):  #this class holds two checks all child classes will inherit.
    kind = None              #each class sets this to the data type it is testing (e.g. "emails", "urls", etc.)
    def assertMatches(self, text, expected):
        self.assertEqual(extract(text, self.kind), expected)

    def assertNoMatch(self, text):
        self.assertEqual(extract(text, self.kind), [], f"unexpected match in {text!r}")


class TestEmail(PatternTestCase):  #class for testing email patterns, inherits from PatternTestCase
    kind = "emails" #this tells helpers above that this class is testing email patterns

    def test_valid(self):
        self.assertMatches("user@example.com", ["user@example.com"])
        self.assertMatches(
            "firstname.lastname@company.co.uk", ["firstname.lastname@company.co.uk"]
        )
        self.assertMatches("a+tag@mail.example.org", ["a+tag@mail.example.org"])

    def test_invalid(self):
        for bad in ["user@", "@example.com", "user@.com", "user@example..com", "plain text"]:
            self.assertNoMatch(bad)

    def test_multiple_in_sentence(self):
        text = "Write to a@b.com, or c.d@e.org."
        self.assertMatches(text, ["a@b.com", "c.d@e.org"])


class TestURL(PatternTestCase):   # this is a class for testing URL patterns, inherits from PatternTestCase
    kind = "urls"

    def test_valid(self):
        self.assertMatches("https://www.example.com", ["https://www.example.com"])
        self.assertMatches(
            "https://subdomain.example.org/page", ["https://subdomain.example.org/page"]
        )
        self.assertMatches("http://example.com:8080/a?b=1", ["http://example.com:8080/a?b=1"])

    #below are some invalid cases for URL patterns, which should not match  
    def test_invalid(self):
        for bad in ["www.example.com", "http://", "https://", "example.com", "ftp://example.com"]:
            self.assertNoMatch(bad)

    def test_trailing_punctuation_excluded(self):
        self.assertMatches("See https://example.com/page.", ["https://example.com/page"])
        self.assertMatches("(https://example.com)", ["https://example.com"])


#below is a class for testing phone number patterns, inherits from PatternTestCase
class TestPhone(PatternTestCase):
    kind = "phone_numbers"  #this tells helpers above that this class is testing phone number patterns

    def test_valid_formats(self): #this method tests valid phone number formats and checks if they match the expected output
        self.assertMatches("(123) 456-7890", ["(123) 456-7890"])
        self.assertMatches("123-456-7890", ["123-456-7890"])
        self.assertMatches("123.456.7890", ["123.456.7890"])

    def test_invalid(self): #this method tests invalid phone number formats and checks if they do not match any output
        for bad in ["123-456.7890", "123-45-67890", "12-345-6789", "1234567890", "(123)456 7890"]:
            self.assertNoMatch(bad) #this self.assertNoMatch method is inherited from PatternTestCase and checks if the given text does not match any expected output for the phone number pattern.

    def test_not_inside_credit_card(self):
        self.assertNoMatch("1234-5678-9012-3456") #this self.assertNoMatch method is inherited from PatternTestCase and checks if the given text does not match any expected output for the phone number pattern. In this case, it checks that a phone number pattern does not match a credit card number.

#the following class tests credit card patterns, inherits from PatternTestCase
class TestCreditCard(PatternTestCase):
    kind = "credit_cards"   #this tells helpers above that this class is testing credit card patterns

    def test_valid(self):
        self.assertMatches("1234 5678 9012 3456", ["1234 5678 9012 3456"])
        self.assertMatches("1234-5678-9012-3456", ["1234-5678-9012-3456"])

    def test_invalid(self):  #this method tests invalid credit card formats and checks if they do not match any output
        for bad in [
            "1234 5678-9012 3456",   # mixed separators
            "1234 5678 9012 345",    # 15 digits
            "1234 5678 9012 34567",  # 17 digits
            "1234567890123456",      # no separators
        ]:
            self.assertNoMatch(bad)

#the following class tests time patterns, inherits from PatternTestCase
class TestTime(PatternTestCase):
    kind = "times"

    def test_valid(self): #these time formats are valid and should match the expected output
        self.assertMatches("14:30", ["14:30"])
        self.assertMatches("2:30 PM", ["2:30 PM"])
        self.assertMatches("12:30 PM", ["12:30 PM"])
        self.assertMatches("11:15am", ["11:15am"])
        self.assertMatches("00:00", ["00:00"])
        self.assertMatches("23:59", ["23:59"])

    def test_invalid(self): #these time formats are invalid and should not match any output
        for bad in ["25:00", "14:60", "13:00 PM", "7:5", "99:99"]:
            self.assertNoMatch(bad) #this self.assertNoMatch method checks if the given text does not match any expected output for the time pattern.

    def test_mixed_formats_in_one_string(self):
        self.assertMatches("Open 09:00, lunch 12:30 PM", ["09:00", "12:30 PM"])

#this class tests HTML tag patterns, inherits from PatternTestCase
class TestHTMLTag(PatternTestCase):
    kind = "html_tags"

    def test_valid(self):
        self.assertMatches("<p>", ["<p>"])
        self.assertMatches('<div class="example">', ['<div class="example">'])
        self.assertMatches(
            '<img src="image.jpg" alt="description">',
            ['<img src="image.jpg" alt="description">'],
        )
        self.assertMatches("</div>", ["</div>"])
        self.assertMatches("<br/>", ["<br/>"])

    def test_invalid(self):
        for bad in ["<>", "< p>", "3 < 5 > 2", "<3", "plain text"]:
            self.assertNoMatch(bad)

    def test_multiple_tags(self):
        self.assertMatches("<p>Hi</p>", ["<p>", "</p>"])

#this class tests hashtag patterns, inherits from PatternTestCase
class TestHashtag(PatternTestCase):
    kind = "hashtags"

    def test_valid(self):
        self.assertMatches("#example", ["#example"])
        self.assertMatches("#ThisIsAHashtag", ["#ThisIsAHashtag"])
        self.assertMatches("love #regex_2026 today", ["#regex_2026"])
        self.assertMatches("#100DaysOfCode", ["#100DaysOfCode"])

    def test_invalid(self):
        for bad in ["#", "# space", "page#section", "&#39;", "#123"]:
            self.assertNoMatch(bad)

#this class tests currency patterns, inherits from PatternTestCase
class TestCurrency(PatternTestCase):
    kind = "currency"

    def test_valid(self):
        self.assertMatches("$19.99", ["$19.99"])
        self.assertMatches("$1,234.56", ["$1,234.56"])
        self.assertMatches("$5", ["$5"])
        self.assertMatches("$1,000,000.00", ["$1,000,000.00"])

    def test_invalid(self):
        for bad in ["$1,23.4", "$.99", "$19.999", "19.99", "$"]:
            self.assertNoMatch(bad)

    def test_sentence_end(self):
        self.assertMatches("It costs $19.99.", ["$19.99"])

    def test_followed_by_comma(self):
        self.assertMatches("Prices: $19.99, $1,234.56, $5 and $7", ["$19.99", "$1,234.56", "$5", "$7"])

#this class tests the extract_all function, which runs every pattern on a given text and returns a dictionary of matches for each data type
class TestExtractAll(unittest.TestCase): 
    def test_returns_every_type(self):
        result = extract_all("hi a@b.com #tag $5")  #this line calls the extract_all function with a sample text containing an email, a hashtag, and a currency amount. The result is expected to be a dictionary containing matches for each data type defined in the PATTERNS dictionary.
        self.assertEqual(
            set(result),
            {"emails", "urls", "phone_numbers", "credit_cards",
             "times", "html_tags", "hashtags", "currency"},
        )  #this line checks if the keys of the result dictionary match the expected set of data types defined in the PATTERNS dictionary. It uses the set() function to convert the keys of the result dictionary into a set and compares it with the expected set of data types. If they are not equal, the test will fail.
        self.assertEqual(result["emails"], ["a@b.com"])

    def test_unique_option(self): #this method tests the unique option of the extract function, which drops duplicates while keeping first-seen order. It checks if the extract function returns the expected output when the unique option is set to True.
        self.assertEqual(extract("#a #a #b", "hashtags", unique=True), ["#a", "#b"])

    def test_unknown_kind(self):   #this method tests the behavior of the extract function when an unknown data type is passed as the kind argument. It checks if the function raises a KeyError with the expected error message.
        with self.assertRaises(KeyError):
            extract("text", "nonsense")

    def test_empty_string(self):
        self.assertTrue(all(v == [] for v in extract_all("").values()))


if __name__ == "__main__":
    unittest.main()
#this condition checks if the script is being run directly (not imported as a module) and calls unittest.main() to run all the test cases defined in the script.