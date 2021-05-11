from collections import defaultdict
import numpy as np
from scipy.spatial.distance import hamming

def tolerance_principle(n, c, xi=None, print_threshold=False):
    if xi == None:
        xi = n - c
    if print_threshold and xi > n / np.log(n):
        print(f'{xi} <= {n / np.log(n)}')
    return c > 2 and xi <= n / np.log(n) and c > n / 2

def load_word_to_ipa():
    word_to_ipa = dict()
    with open('../data/english/ipa.txt', 'r') as f:
        for line in f:
            word, ipa = line.strip().split('\t')
            assert(word not in word_to_ipa)
            word_to_ipa[word] = ipa
    return word_to_ipa

def load_pairs(fname, lang, with_freq=False):
    pairs = list()
    feature_space = set()
    freqs = list()
    with open(fname, 'r') as f:
        for line in f:
            if lang == 'german':
                singular, plural, feats, freq = line.strip().split('\t')
                singular = singular.replace(u'ä', 'a').replace(u'ü', 'u').replace(u'ö', 'o').replace(u'Ä', 'A').replace(u'Ü', 'U').replace(u'Ö', 'O')
                plural = plural.replace(u'ä', 'a').replace(u'ü', 'u').replace(u'ö', 'o').replace(u'Ä', 'A').replace(u'Ü', 'U').replace(u'Ö', 'O')
                feature_space.update(feats.split(';'))
                pairs.append((singular, plural, tuple(feats.split(';'))))
                freqs.append(float(freq))
            elif lang == 'english-quant':
                _, lemma, _, inflected, feats, _ = line.strip().split('\t')
                feature_space.update(feats.split(';'))
                pairs.append((lemma, inflected, tuple(feats.split(';'))))
    if with_freq:
        return pairs, feature_space, freqs
    return pairs, feature_space

def load_german_CHILDES(with_feats=False):
    pairs = list()
    feature_space = set()
    with open('../data/german/CHILDES-DE.txt', 'r') as f:
        for line in f:
            if line.startswith('singular\tplural'):
                continue
            singular, plural, feats = line.strip().split('\t')
            singular = singular.replace(u'ä', 'a').replace(u'ü', 'u').replace(u'ö', 'o').replace(u'Ä', 'A').replace(u'Ü', 'U').replace(u'Ö', 'O')
            plural = plural.replace(u'ä', 'a').replace(u'ü', 'u').replace(u'ö', 'o').replace(u'Ä', 'A').replace(u'Ü', 'U').replace(u'Ö', 'O')
            feats = tuple(sorted(set(feats.split(',')).difference({'Mono-N', 'RFS', 'C'} if not with_feats else {'Mono-N', 'C'})))
            feature_space.update(feats)
            pairs.append((singular, plural, feats))
    return pairs, feature_space

def hamming_distance(w1, w2):
    w1, w2 = list(w1), list(w2)
    while len(w1) > len(w2):
        w2 = ['0'] + w2
    while len(w1) < len(w2):
        w1 = ['0'] + w1
    return hamming(w1, w2)

def most_freq(l):
    item_to_count = defaultdict(int)
    for item in l:
        item_to_count[item] += 1
    argmax = None
    max_val = -1000
    for item, count in item_to_count.items():
        if count > max_val:
            argmax = item
            max_val = count
    return argmax