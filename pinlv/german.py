import os
import re

from typing import List, Dict, Any

import pandas as pd


# TODO: Move this to a common file
POS_MAPPING = {
    "adj": "adjective",
    "adv": "adverb",
    "aux": "auxiliary",
    "clas": "classifier",
    "conj": "conjunction",
    "idiom": "idiom",
    "interj": "interjection",
    "loc": "locality",
    "n": "noun",
    "num": "numeral",
    "ono": "onomatopoeia",
    "part": "particle",
    "place": "place",
    "pref": "prefix",
    "prep": "preposition",
    "pron": "pronoun",
    "suf": "suffix",
    "time": "time",
    "v": "verb",
}

DATA_DIR = "data"
ROUTLEDGE_GERMAN_WORD_FREQUENCY_RELATIVE_PATH = "routledge_german_word_frequency.txt"
ROUTLEDGE_GERMAN_WORD_FREQUENCY_FULL_PATH = os.path.join(
    DATA_DIR, ROUTLEDGE_GERMAN_WORD_FREQUENCY_RELATIVE_PATH
)

def parse_file(contents: str = ROUTLEDGE_GERMAN_WORD_FREQUENCY_FULL_PATH) -> List[Dict[str, Any]]:
    # Split the file into lines
    lines = contents.strip().split('\n')

    # Regular expression to match the start of a new entry
    entry_start_re = re.compile(r'^(\d+)\s+([\wäöüß]+)\s+(\d+|art|conj|prep|verb|pron|part|adv)\s+')

    # List to hold all entries
    entries = []

    # Temporary storage for the current entry being parsed
    current_entry = {}

    for line in lines:
        # Check if the line is the start of a new entry
        if entry_start_re.match(line):
            # If there's an entry being built, save it before starting a new one
            if current_entry:
                entries.append(current_entry)
                current_entry = {}

            # Parse the main components of the entry
            parts = line.split('\t')
            # Assuming the first 4 fields are always present as described
            current_entry = {
                'rank frequency': parts[0],
                'headword': parts[1],
                'part of speech': parts[2],
                'English equivalent': parts[3],
                'sample sentences': [parts[4] if len(parts) > 4 else ""],
                'translations': [parts[5] if len(parts) > 5 else ""],
                'metrics': parts[-1] if parts[-1].strip().startswith('|') else ""
            }
        else:
            # Additional meanings or sample sentences for the current entry
            parts = line.split('\t')
            if len(parts) > 4 and 'sample sentences' in current_entry:  # Additional meanings
                current_entry['sample sentences'].append(parts[4] if len(parts) > 4 else "")
                current_entry['translations'].append(parts[5] if len(parts) > 5 else "")
                # Update metrics if present
                if parts[-1].strip().startswith('|'):
                    current_entry['metrics'] = parts[-1]
            elif parts[-1].strip().startswith('|'):  # Just metrics update, rare case
                current_entry['metrics'] = parts[-1]

    # Don't forget to add the last entry
    if current_entry:
        entries.append(current_entry)

    return entries
