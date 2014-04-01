#!/usr/bin/env python
'''Ultra simple summarizer'''

# Algorithm:
# 1. For each word, caluclate it's frequency in the document
# 2. For each sentence in the document
#       score(sentence) = sum([freq(word) for word in sentence])
# 3. Print X top sentences such that their size < MAX_SUMMARY_SIZE
# See http://en.wikipedia.org/wiki/Sentence_extraction for more

__author__ = 'Miki Tebeka <miki.tebeka@gmail.com>'

from collections import defaultdict
import re

MAX_SUMMARY_SIZE = 300


def tokenize(text):
    '''Very simple white space tokenizer, in real life we'll be much more
    fancy.
    '''
    return text.split()


def split_to_sentences(text):
    '''Very simple spliting to sentences by [.!?] and paragraphs.
    In real life we'll be much more fancy.
    '''
    sentences = []
    start = 0

    # We use finditer and not split since we want to keep the end
    for match in re.finditer('(\s*[.!?]\s*)|(\n{2,})', text):
        sentences.append(text[start:match.end()].strip())
        start = match.end()

    if start < len(text):
        sentences.append(text[start:].strip())

    return sentences


def token_frequency(text):
    '''Return frequency (count) for each token in the text'''
    frequencies = defaultdict(int)
    for token in tokenize(text):
        frequencies[token] += 1

    return frequencies


def sentence_score(sentence, frequencies):
    return sum((frequencies[token] for token in tokenize(sentence)))


def create_summary(sentences, max_length):
    summary = []
    size = 0
    for sentence in sentences:
        summary.append(sentence)
        size += len(sentence)
        if size >= max_length:
            break

    summary = summary[:max_length]
    return '\n'.join(summary)


def summarize(text, max_summary_size=MAX_SUMMARY_SIZE):
    frequencies = token_frequency(text)
    sentences = split_to_sentences(text)
    sentences.sort(key=lambda s: sentence_score(s, frequencies), reverse=1)
    summary = create_summary(sentences, max_summary_size)

    return summary