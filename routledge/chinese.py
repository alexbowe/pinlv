import os

import pandas as pd

DATA_DIR = "data"
ROUTLEDGE_CHINESE_WORD_FREQUENCY_FILE = "routledge_chinese_word_frequency.txt"

# TODO: Write this as a Context Free Grammar and use NLTK (?) to parse it.
# Here is a tool to help visualize this: https://regex101.com/r/yzMkTg/1
CHINESE_EXAMPLE_SPLITTING_REGEX = (
    r"^(.*[\u4e00-\u9fff。！？?：.…]+[”]?)\s?([“]?[A-Za-z].*)$"
)


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
        .str.contains(r"[A-Za-z]]")
        .any()
    )
    assert not df["example_english"].str.contains(r"[\u4e00-\u9fff]").any()


def map_or_raise_exception(mapping):
    return lambda input: mapping[input]


def load_routledge_chinese_word_frequency_data_from_file(filepath):
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
    df["headword_traditional"] = df["headword_traditional"].str.extract(r"\[(.+)\]")
    df["pinyin"] = df["pinyin"].str.extract(r"/([^/]+)/")
    df["hsk_level"] = df["hsk_level"].str.extract(r"\((\d+)\)")
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


def load_routledge_chinese_word_frequency_data():
    filepath = os.path.join(DATA_DIR, ROUTLEDGE_CHINESE_WORD_FREQUENCY_FILE)
    return load_routledge_chinese_word_frequency_data_from_file(filepath)
