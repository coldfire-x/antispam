# -*- coding: utf8 -*-

from __future__ import unicode_literals

import re
import os
import codecs


class BaseCLeaner(object):
    """base cleaner class."""

    def clean(self):
        raise NotImplemented


class LowerCleaner(BaseCLeaner):
    """convert all chars to lower."""

    def clean(self, sentence):
        return sentence.lower()


class PunctuationCleaner(BaseCLeaner):
    """remove punctuations from txt."""

    def __init__(self, puns):
        self._punctuations = puns

    def clean(self, sentence):
        segs = re.sub(r'\s+', '', sentence)
        result = u''
        for w in segs:
            if w in self._punctuations:
                continue
            result += w
        return result


class Resource(object):
    """load data sources."""

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    def __init__(self):
        self._punctuation = None
        self._spam = None
        self._normal = None
        self._high_freq = None

    def _load_from_file(self, path):
        path = os.path.join(self.data_dir, path)
        with codecs.open(path, encoding='utf8') as f:
            data = []
            for line in f.readlines():
                line = line.strip()
                if line: data.append(line)
            return data

    def get_normal(self):
        if self._normal: return self._normal
        self._normal = self._load_from_file('train_set_normal.txt')
        return self._normal

    def get_spam(self):
        if self._spam: return self._spam
        self._spam = self._load_from_file('train_set_spam.txt')
        return self._spam

    def get_punctuation(self):
        """load punctuations"""
        if self._punctuation: return self._punctuation
        self._punctuation = self._load_from_file('punctuation.txt')[0]
        return self._punctuation

    def get_high_freq_words(self):
        if self._high_freq: return self._high_freq
        self._high_freq = self._load_from_file('high_freq_words.txt')
        return self._high_freq


r_manager = Resource()
