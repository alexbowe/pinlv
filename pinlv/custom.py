import os
import glob
import itertools as it

import nltk
import pandas as pd

from nltk import FreqDist, WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)


def lemmatize_words(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text.lower())
    pos_tagged_tokens = nltk.pos_tag(tokens)
    lemmatized_words = [
        (lemmatizer.lemmatize(word), pos)
        for word, pos in pos_tagged_tokens
        if word.isalpha()
    ]
    return lemmatized_words


def calculate_word_frequencies(file_paths):
    word_frequency = FreqDist()

    for file_path in file_paths:
        with open(file_path, "r") as file:
            text = file.read()
            lemmatized_words = lemmatize_words(text)
            word_frequency.update(lemmatized_words)

    sorted_by_frequency = sorted(
        word_frequency.items(), key=lambda x: x[1], reverse=True
    )
    return sorted_by_frequency


def print_obsidian_frequencies():
    # Specify the list of file paths
    directory = "/Users/alexbowe/Documents/Obsidian"
    file_paths = glob.glob(os.path.join(directory, "**/*.md"), recursive=True)
    frequencies = calculate_word_frequencies(file_paths)
    total = sum(f for _, f in frequencies)
    cumulative_frequencies = list(it.accumulate(f for _, f in frequencies))

    for i, ((w, f), cf) in enumerate(zip(frequencies, cumulative_frequencies)):
        print(f"{i+1:03}\t{w}\t{f}\t{f/total:.2%}\t{cf/total:.2%}")
        if cf / total >= 0.5:
            break


# TODO: Make dataframes of arbitrary text file globs
