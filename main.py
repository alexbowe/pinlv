from pinlv.parsers.routledge import load_routledge_chinese_word_frequency_data


df = load_routledge_chinese_word_frequency_data()
print(df.head(10))

# TODO: Load the symbol frequencies
# TODO: Load the radical database
# TODO: Make dataframes of arbitrary text file globs
# TODO: Add ability to adjust frequencies to prioritize learning song lyrics (or other media)
# TODO: Translate my personal data and create a table to modify frequencies
# TODO: Build a graph with radicals, hanzi, words, and sentences
# TODO: Use pagerank to spread the ranks (compare the outcomes)
# TODO: Do a toposort and sort by the pagerank (somehow)
# TODO: Add mnemonics for the radicals (maybe taken from pandaverse)
