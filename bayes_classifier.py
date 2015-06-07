# -*- coding: utf8 -*-

import math

import jieba

import resource_loader


spam = resource_loader.r_manager.get_spam()
normal = resource_loader.r_manager.get_normal()
puncs = resource_loader.r_manager.get_punctuation()
high_freq = resource_loader.r_manager.get_high_freq_words()

freq_spam = {}
freq_normal = {}

puncs_cleaner = resource_loader.PunctuationCleaner(puncs)
lower_cleaner = resource_loader.LowerCleaner()

spam_c = []
for line in spam:
    line = puncs_cleaner.clean(line)
    if not line: continue
    line = lower_cleaner.clean(line)
    spam_c.append(line)

normal_c = []
for line in normal:
    line = puncs_cleaner.clean(line)
    if not line: continue
    line = lower_cleaner.clean(line)
    normal_c.append(line)

jieba.load_userdict('antispam/data/jieba_userdict.txt')
#jieba.load_userdict('data/jieba_userdict.txt')


for line in spam_c:
    for seg in jieba.cut(line):
        seg = seg.strip()
        if not seg or seg in high_freq: continue

        if seg in freq_spam:
            freq_spam[seg] += 1

        else:
            freq_spam[seg] = 1

for seg in freq_spam:
    freq_spam[seg] = freq_spam[seg] * 1.0 / len(spam_c)

print '*' * 10,  'spam ', '*' * 10
for i in sorted(freq_spam, key=lambda x: freq_spam[x], reverse=True)[:10]:
    print i, freq_spam[i]


for line in normal_c:
    for seg in jieba.cut(line):
        seg = seg.strip()
        if not seg or seg in high_freq: continue

        if seg in freq_normal:
            freq_normal[seg] += 1

        else:
            freq_normal[seg] = 1

for seg in freq_normal:
    freq_normal[seg] = freq_normal[seg] * 1.0 / len(normal_c)

print '*' * 10,  'normal', '*' * 10
for i in sorted(freq_normal, key=lambda x: freq_normal[x], reverse=True)[:10]:
    print i, freq_normal[i]


def prob(word):
    # return as (normal prob, spam prob)
    p2 = 0.001
    if word in freq_spam:
        p2 = freq_spam[word]

    p1 = p2
    if word in freq_normal:
        p1 = freq_normal[word]

    return p1, p2


def classify(line):
    raw_line = line
    line = puncs_cleaner.clean(line.decode('utf8'))
    if not line: return 'spam'

    line = lower_cleaner.clean(line)
    segs = jieba.cut(line)

    p = 1.0
    notp = 1.0
    for seg in segs:
        seg = seg.strip()
        if not seg or seg in high_freq: continue

        # return as (normal prob, spam prob)
        np, sp = prob(seg)
        print 'seg ', seg
        print 'prob ', np, ' ', sp

        p *= np
        notp *= sp

        #print 'p ', p
        #print 'notp ', notp

    try:
        final_p = notp/(p+notp)
        print 'final prob ', final_p

        if final_p < 0.9:
            print 'normal'
            print final_p
            print raw_line
            print
        else:
            print 'spam'
            print final_p
            print raw_line
            print
            raw_input('continue ?')
    except:
        pass


if '__main__' == __name__:
    while True:
        print classify(line)
