from pinlv.chinese import load_routledge_chinese_word_frequency_data, load_radical_meanings, load_radical_mapping, load_routledge_chinese_character_frequency_data


#df = load_routledge_chinese_word_frequency_data()
#print(df.head(10))

"""
total = 0
threshold = 0.5
for i, row in df.iterrows():
    total += row.normalized_frequency
    cumulative_freq = total/df.normalized_frequency.sum()
    print(f"{i}: {row.headword_simplified}\t{row.pinyin}\t{row.english_gloss}\t{cumulative_freq}")
    if cumulative_freq >= threshold: break
"""

# TODO: Load the symbol frequencies
# TODO: Load the radical database
# TODO: Make dataframes of arbitrary text file globs
# TODO: Add ability to adjust frequencies to prioritize learning song lyrics (or other media)
# TODO: Translate my personal data and create a table to modify frequencies
# TODO: Build a graph with radicals, hanzi, words, and sentences
# TODO: Use pagerank to spread the ranks (compare the outcomes)
# TODO: Do a toposort and sort by the pagerank (somehow)
# TODO: Add mnemonics for the radicals (maybe taken from pandaverse)

#x = load_radical_mapping()
x = load_radical_meanings()
#x = load_routledge_chinese_character_frequency_data()
#hw = x[0]["headwords"]
print(x)