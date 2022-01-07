import pandas as pd
from collections import Counter
import re
import numpy as np




def generate_df(path='words_alpha_clean.txt'):
    # open and process
    words = open(path)
    word_list = words.readlines()
    word_list_clean = [word.replace('\n', '') for word in word_list[1:]]
    word_list_5 = [word for word in word_list_clean if len(word)==5]

    # generate character frequency dict
    char_freqs = {}
    for word in word_list_5:
        for char in word:
            if char in char_freqs.keys():
                char_freqs[char] += 1
            else:
                char_freqs[char] = 1
    # normalize
    chars_total = len(word_list_5)*5
    for key in char_freqs.keys():
        char_freqs[key] = char_freqs[key]/chars_total

    # calculate word score to test likely characters earlier
    scores_list = [word_score(word, char_freqs) for word in word_list_5]

    words_df = pd.DataFrame({'word':word_list_5, 'score':scores_list}).drop_duplicates()
    return words_df


def word_score(word, char_freqs):
    # calculate score based on letter frequency
    unique_chars = list(set(word)) # test as many unique characters as possible
    freqs_list = [char_freqs[char] for char in unique_chars]
    score = 0
    for f in freqs_list:
        score += f # simple addition optimal?
    return score


def generate_regex(contained, excluded, position):
    re_list = []
    if len(excluded)>0:
        re_list.append(f'^[^{excluded}]*$')
    for char in contained:
        re_list.append(f'.*{char}')
    re_list.append(position)

    regex = ''
    for re_str in re_list:
        regex += f'(?={re_str})'
    return regex


def show_words(df, contained, excluded, position):
    regex = generate_regex(contained, excluded, position)
    print(df[df['word'].str.contains(regex)].sort_values(by=['score'], ascending=False).head())