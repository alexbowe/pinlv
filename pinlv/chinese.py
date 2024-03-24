import os
import re

import pandas as pd

DATA_DIR = "data"
ROUTLEDGE_CHINESE_WORD_FREQUENCY_RELATIVE_PATH = "routledge_chinese_word_frequency.txt"
ROUTLEDGE_CHINESE_CHARACTER_FREQUENCY_RELATIVE_PATH = (
    "routledge_chinese_character_frequency.txt"
)
RADICAL_MEANINGS_RELATIVE_PATH = "radical_meanings.txt"
KRADFILE_RELATIVE_PATH = "kradfile-u.txt"
ROUTLEDGE_CHINESE_WORD_FREQUENCY_FULL_PATH = os.path.join(
    DATA_DIR, ROUTLEDGE_CHINESE_WORD_FREQUENCY_RELATIVE_PATH
)
ROUTLEDGE_CHINESE_CHARACTER_FREQUENCY_FULL_PATH = os.path.join(
    DATA_DIR, ROUTLEDGE_CHINESE_CHARACTER_FREQUENCY_RELATIVE_PATH
)
RADICAL_MEANINGS_FULL_PATH = os.path.join(DATA_DIR, RADICAL_MEANINGS_RELATIVE_PATH)
KRADFILE_FULL_PATH = os.path.join(DATA_DIR, KRADFILE_RELATIVE_PATH)

CHINESE_CHARACTERS = "\u4e00-\u9fff"
CHINESE_PUNCTUATION = "。！？?：.…"
ENGLISH_CHARACTERS = "A-Za-z"
CLOSE_QUOTE = "”"
OPEN_QUOTE = "“"

# The example column mixes Chinese and English, so we need to split it.
# Unfortunately, spaces are occasionally used in the Chinese sentences,
# so calling split() doesn't help much. And not every English sentence starts
# with a capital letter, and sometimes starts with a quote. It can be difficult
# to determine if the quote belogs to the Chinese sentence or the English
# sentence, since there isn't always a space separating them. Fortunately,
# they distinguish betweeen open and close quotes, so we can use a regex.
# This is a mess, as regexes often are, and would perhaps be better handled
# by a Context Free Grammar. Howewver, this parses the entire Routledge
# Chinese Word Frequency List, so it's fine for now.
# Here is a tool to help visualize it: https://regex101.com/r/yzMkTg/1
CHINESE_EXAMPLE_SPLITTING_REGEX = rf"^(.*[{CHINESE_CHARACTERS}{CHINESE_PUNCTUATION}]+[{CLOSE_QUOTE}]?)\s?([{OPEN_QUOTE}]?[{ENGLISH_CHARACTERS}].*)$"


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


def run_tests(df):
    assert df["example_simplified_chinese"].notnull().all()
    assert df["example_english"].notnull().all()
    assert not df["example_simplified_chinese"].eq("").any()
    assert not df["example_english"].eq("").any()
    assert (
        not df["example_simplified_chinese"]
        .str.contains(rf"[{ENGLISH_CHARACTERS}]]")
        .any()
    )
    assert not df["example_english"].str.contains(rf"[{CHINESE_CHARACTERS}]").any()


def map_or_raise_exception(mapping):
    return lambda input: mapping[input]


def load_routledge_chinese_word_frequency_data(
    filepath=ROUTLEDGE_CHINESE_WORD_FREQUENCY_FULL_PATH,
):
    num_header_lines = 4
    df = pd.read_csv(
        filepath,
        sep="\t",
        header=None,
        skiprows=num_header_lines,
        names=[
            "frequency_rank",
            "headword_simplified",
            "headword_traditional",
            "pinyin",
            "hsk_level",
            "part_of_speech",
            "english_gloss",
            "example",
            "normalized_frequency",
        ],
        skip_blank_lines=True,
    )

    # Adjust the index to match the rank
    df.index = range(1, len(df) + 1)
    # Frequency Rank is redundant now
    df = df.drop(columns=["frequency_rank"])

    # Clean up formatting of columns
    df["headword_traditional"] = df["headword_traditional"].str.strip("[]")
    df["pinyin"] = df["pinyin"].str.strip("/")
    df["hsk_level"] = df["hsk_level"].str.strip("()")
    df["part_of_speech"] = df["part_of_speech"].apply(
        map_or_raise_exception(POS_MAPPING)
    )

    df[["example_simplified_chinese", "example_english"]] = df["example"].str.extract(
        CHINESE_EXAMPLE_SPLITTING_REGEX
    )
    del df["example"]

    df["example_simplified_chinese"] = df["example_simplified_chinese"].str.strip()
    df["example_english"] = df["example_english"].str.strip()

    df[
        [
            "normalized_frequency",
            "dispersion_index",
            "usage_rate",
            "optional_register_code",
        ]
    ] = df["normalized_frequency"].str.split("|", expand=True)

    # Set the dtype for the numeric columns
    df["normalized_frequency"] = pd.to_numeric(df["normalized_frequency"])
    df["dispersion_index"] = pd.to_numeric(df["dispersion_index"])
    df["usage_rate"] = pd.to_numeric(df["usage_rate"])

    run_tests(df)

    return df


def load_routledge_chinese_character_frequency_data(
    filename=ROUTLEDGE_CHINESE_CHARACTER_FREQUENCY_FULL_PATH,
):
    def parse_line(line):
        line = line.strip()
        parts = line.split("\t")
        frequency_rank = int(parts[0])
        simplified_chinese = parts[1]
        traditional_chinese = parts[2].strip("[]")
        pinyin = parts[3].strip("/")
        hsk_level = int(parts[4].strip("()")) if len(parts) > 4 and parts[4] else None
        headwords = parts[5:]
        headwords = [
            re.match(rf"^([{CHINESE_CHARACTERS}\[\]]+)(\d+)$", headword)
            for headword in headwords
        ]
        headwords = [
            {
                "simplified_chinese": match.group(1),
                "frequency_rank": int(match.group(2)),
            }
            for match in headwords
            if match
        ]
        return {
            "frequency_rank": frequency_rank,
            "simplified_chinese": simplified_chinese,
            "traditional_chinese": traditional_chinese,
            "pinyin": pinyin,
            "hsk_level": hsk_level,
            "headwords": headwords,
        }

    with open(filename, "r") as f:
        lines = f.readlines()
    result = [parse_line(line) for line in lines[2:] if line]
    return result


def load_radical_meanings(filename=RADICAL_MEANINGS_FULL_PATH):
    with open(filename, "r") as f:
        lines = f.readlines()
    data = [
        (radical.strip(), pd.Series(meaning.strip().split("/")))
        for radical, meaning in [line.split(":") for line in lines]
    ]
    df = pd.DataFrame(data, columns=["Radical", "Meaning"])
    return df


def load_radical_mapping(filename=KRADFILE_FULL_PATH):
    with open(filename, "r") as f:
        lines = f.readlines()
    lines = [line.rstrip() for line in lines if not line.startswith("#")]
    return {
        hanzi.strip(): radicals.strip().split()
        for hanzi, radicals in [line.split(":") for line in lines]
    }
