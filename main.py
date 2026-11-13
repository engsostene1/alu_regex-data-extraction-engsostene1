""" extract every supported data type from a text file.

how to use :
    python main.py                 # uses sample_input.txt
    python main.py path/to/file    # uses any text file
"""

import sys

from extractor import extract_all

LABELS = {
    "emails": "Email addresses",
    "urls": "URLs",
    "phone_numbers": "Phone numbers",
    "credit_cards": "Credit card numbers",
    "times": "Times",
    "html_tags": "HTML tags",
    "hashtags": "Hashtags",
    "currency": "Currency amounts",
}

#this script extracts every supported data type from a text file. It can be run from the command line, either using the default sample_input.txt file or specifying a different text file as an argument. The results are printed to the console, showing the number of matches found for each data type along with the matched items.
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_input.txt" #this line checks if a command-line argument is provided. If so, it uses that argument as the path to the text file; otherwise, it defaults to "sample_input.txt". This allows the user to specify a different text file when running the script.

    #this opens the specified text file in read mode with UTF-8 encoding. The 'with' statement ensures that the file is properly closed after reading, even if an error occurs. The file handle is assigned to the variable 'handle'.
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    #check if the text is empty. If it is, print a message indicating that the file is empty and return from the function. This prevents further processing on an empty string.
    results = extract_all(text)
    for kind, matches in results.items():
        print(f"\n{LABELS[kind]} ({len(matches)} found)") #this line prints the label for the current data type (e.g., "Email addresses") along with the number of matches found in parentheses. It uses an f-string to format the output, and len(matches) gives the count of matches for that data type.
        print("-" * 40)
        for item in matches:
            print(f"  {item}")


if __name__ == "__main__":
    main()