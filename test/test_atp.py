import unittest
import numpy as np
import glob

import sys
sys.path.append('../src/')
from atp import ATP
from utils import load_pairs, load_word_to_ipa

class TestATP(unittest.TestCase):
    def test_init(self):
        tp = ATP(feature_space={'PST'})

    def test_maximize_productivity_1(self):
        tp = ATP(feature_space={'PRS', 'PST', '1', '2', '3'})
        p1, p2, p3, p4, p5, p6 = ('walk', 'walked', 'PST,3'), \
                                 ('sprint', 'sprinted', 'PST,1'), \
                                 ('run', 'ran', 'PST,1'), \
                                 ('walk', 'walk', 'PRS,2'), \
                                 ('think', 'thinks', 'PRS,3'), \
                                 ('quack', 'quacked', 'PST,2')
        _pairs = [p1, p2, p3, p4, p5, p6]
        y1, y2, y3, y4, y5, y6 = '-ed', '-ed', 'u -> a', '-null', '-s', '-ed'
        _y = [y1, y2, y3, y4, y5, y6]

        feature_space = tp.feature_space
        split_feature, vals_splits, splits_labels = tp.maximize_productivity(_pairs, _y, feature_space)
        assert(split_feature.name in {'PRS', 'PST'})
        assert(len(vals_splits) == 2)
        c1 = sorted(vals_splits[split_feature.name]) == sorted([p4, p5]) and sorted(vals_splits[f'¬{split_feature.name}']) == sorted([p1, p2, p3, p6])
        c2 = sorted(vals_splits[split_feature.name]) == sorted([p1, p2, p3, p6]) and sorted(vals_splits[f'¬{split_feature.name}']) == sorted([p4, p5])
        assert(c1 or c2)

    def _evaluate(self, lang, test_path, tp, no_feats):
        c = 0
        t = 0
        with open(test_path, 'r') as f:
            for line in f:
                if lang == 'english':
                    _, lemma, _, inflected, feats, _ = line.strip().split('\t')
                elif lang == 'german':
                    lemma, inflected, feats, freq = line.strip().split('\t')
                    lemma = lemma.replace(u'ä', 'a').replace(u'ü', 'u').replace(u'ö', 'o').replace(u'Ä', 'A').replace(u'Ü', 'U').replace(u'Ö', 'O')
                    inflected = inflected.replace(u'ä', 'a').replace(u'ü', 'u').replace(u'ö', 'o').replace(u'Ä', 'A').replace(u'Ü', 'U').replace(u'Ö', 'O')
                feats = tuple(feats.split(';'))
                if not no_feats: # use gender
                    pred, was_guess = tp.inflect(lemma, feats, return_whether_guess=True)
                else: # do not use gender
                    pred, was_guess = tp.inflect_no_feat(lemma, ('N/A',), return_whether_guess=True)
                if pred == inflected:
                    c += 1           
                t += 1
        return c / t

    def test_system_german_1(self):
        test_accs = list()
        no_gen_test_accs = list()
        size = 360
        for seed in range(25):
            fname = f'../data/german/quant/train{size}_{seed}.txt'
            test_path = fname.replace(f'train{size}', 'test')
            pairs, feature_space = load_pairs(fname)
            tp = ATP(apply_phonology=False, feature_space=feature_space)
            tp.train(pairs)

            # compute accuracies
            train_acc = self._evaluate('german', fname, tp, no_feats=False)
            assert(train_acc == 1.0)
            test_acc = self._evaluate('german', test_path, tp, no_feats=False)
            test_accs.append(test_acc)
            no_gen_test_acc = self._evaluate('german', test_path, tp, no_feats=True)
            no_gen_test_accs.append(no_gen_test_acc)
        assert(0.75 < np.mean(test_accs) < 0.775)
        assert(0.59 < np.mean(no_gen_test_accs) < 0.61)

    def test_system_german_2(self):
        test_accs = list()
        no_gen_test_accs = list()
        size = 60
        for seed in range(25):
            fname = f'../data/german/quant/train{size}_{seed}.txt'
            test_path = fname.replace(f'train{size}', 'test')
            pairs, feature_space = load_pairs(fname)
            tp = ATP(apply_phonology=False, feature_space=feature_space)
            tp.train(pairs)

            # compute accuracies
            train_acc = self._evaluate('german', fname, tp, no_feats=False)
            assert(train_acc == 1.0)
            test_acc = self._evaluate('german', test_path, tp, no_feats=False)
            test_accs.append(test_acc)
            no_gen_test_acc = self._evaluate('german', test_path, tp, no_feats=True)
            no_gen_test_accs.append(no_gen_test_acc)
        if not 0.54 <= np.mean(test_accs) < 0.57:
            print(0.54, np.mean(test_accs), 0.57)
        assert(0.54 < np.mean(test_accs) < 0.57)
        assert(0.54 < np.mean(no_gen_test_accs) < 0.57)

    def test_system_german_3(self):
        num_seeds = 100
        train_sizes = [50, 100, 200, 300, 400]

        en = [0] * len(train_sizes)
        n = [0] * len(train_sizes)
        e = [0] * len(train_sizes)
        null = [0] * len(train_sizes)
        er = [0] * len(train_sizes)
        s = [0] * len(train_sizes)

        seed = 0 # only one seed for now
        for i, size in enumerate(train_sizes):
            for seed in range(num_seeds):
                fname = f'../data/german/growth/train{size}_{seed}.txt'
                pairs, feature_space = load_pairs(fname)
                tp = ATP(apply_phonology=False, feature_space=feature_space)
                tp.train(pairs)

                suffixes = set()
                for leaf in tp.get_leaves():
                    if leaf.switch_statement.productive:
                        suffix = leaf.switch_statement.default_case.name.split('lemma')[-1].replace(' + ', '')

                        suffixes.add(suffix)
                for suffix in suffixes:
                    if suffix == 'en':
                        en[i] += 1
                    if suffix == 'e':
                        e[i] += 1
                    if suffix == 'n':
                        n[i] += 1
                    if suffix == '':
                        null[i] += 1
                    if suffix == 'er':
                        er[i] += 1
                    if suffix == 's':
                        s[i] += 1

        assert(n == [100, 100, 100, 100, 100])
        assert(en == [0, 0, 100, 100, 100])
        assert(e[1:] == [100, 100, 100, 100])
        assert(25 <= e[0] <= 27)
        assert(null[1:] == [100, 100, 100, 100])
        assert(74 <= null[0] <= 76)
        assert(s[:-2] == [0, 0, 0])
        assert(0 <= s[-2] <= 2)
        assert(14 <= s[-1] <= 16)

    def test_system_german_4(self):
        from utils import load_german_CHILDES
        pairs, features = load_german_CHILDES()
        atp = ATP(feature_space=features)
        atp.train(pairs)
        leaf_names = set()
        for leaf in atp.get_leaves():
            leaf_names.add(leaf.name)

        assert('[e|del|hel]# => inflected = lemma + n' in leaf_names)
        assert('¬[e|del|hel]#,[n|er|gel|kel|sel]# => inflected = lemma + ' in leaf_names)
        assert('¬[e|del|hel]#,¬[n|er|gel|kel|sel]#,M,el# => inflected = lemma + ' in leaf_names)
        assert('¬[e|del|hel]#,¬[n|er|gel|kel|sel]#,M,¬el# => inflected = lemma + e' in leaf_names)
        assert('¬[e|del|hel]#,¬[n|er|gel|kel|sel]#,¬M,[g|r|t]# => inflected = lemma + en' in leaf_names)
        assert('¬[e|del|hel]#,¬[n|er|gel|kel|sel]#,¬M,¬[g|r|t]#,[d|h|i]# => inflected = lemma + er' in leaf_names)
        assert('¬[e|del|hel]#,¬[n|er|gel|kel|sel]#,¬M,¬[g|r|t]#,¬[d|h|i]#,el# => inflected = lemma + n' in leaf_names)
        assert('¬[e|del|hel]#,¬[n|er|gel|kel|sel]#,¬M,¬[g|r|t]#,¬[d|h|i]#,¬el#,[l|s]# => inflected = lemma + e' in leaf_names)
        assert('¬[e|del|hel]#,¬[n|er|gel|kel|sel]#,¬M,¬[g|r|t]#,¬[d|h|i]#,¬el#,¬[l|s]# => inflected = lemma + s' in leaf_names)

    def test_system_english_1(self):
        test_accs = list()
        size = 1000
        for seed in range(10):
            fname = f'../data/english/quant/unimorph_celex0_train{size}_{seed}.txt'
            test_path = fname.replace(f"{fname.split('_')[-2]}", 'test')
            pairs, feature_space = load_pairs(fname)
            tp = ATP(apply_phonology=False, feature_space=feature_space)
            tp.train(pairs)

            # compute accuracies
            train_acc = self._evaluate('english', fname, tp, no_feats=False)
            assert(0.999 <= train_acc <= 1.0)
            test_acc = self._evaluate('english', test_path, tp, no_feats=False)
            test_accs.append(test_acc)

        assert(0.9 < np.mean(test_accs) < 0.92)

    def test_system_english_2(self):
        test_accs = list()
        size = 100
        for seed in range(10):
            fname = f'../data/english/quant/unimorph_celex0_train{size}_{seed}.txt'
            test_path = fname.replace(f"{fname.split('_')[-2]}", 'test')
            pairs, feature_space = load_pairs(fname)
            tp = ATP(apply_phonology=False, feature_space=feature_space)
            tp.train(pairs)

            # compute accuracies
            train_acc = self._evaluate('english', fname, tp, no_feats=False)
            assert(0.999 <= train_acc <= 1.0)
            test_acc = self._evaluate('english', test_path, tp, no_feats=False)
            test_accs.append(test_acc)

        if not 0.51 < np.mean(test_accs) < 0.583:
            print(0.51, np.mean(test_accs), 0.583)
        assert(0.51 < np.mean(test_accs) < 0.583)

    def test_system_english_3(self):
        num_children = 4

        ing = [0] * 20
        s = [0] * 20
        d = [0] * 20

        word_to_ipa = load_word_to_ipa()

        for child in range(num_children):
            vocabs = list(glob.glob(f'../data/english/growth/child-{child}/*.txt'))
            vocabs = sorted(vocabs, key=lambda it: int(it.split('/')[-1].split('.txt')[0]))
            for i, vocab in enumerate(vocabs):
                pairs = list()
                feature_space = set()
                with open(vocab, 'r') as f:
                    for line in f:
                        lemma, inflected, feats = line.strip().split()
                        lemma_ipa = word_to_ipa[lemma]
                        inflected_ipa = word_to_ipa[inflected]
                        feature_space.update(feats.split(';'))
                        pairs.append((lemma_ipa, inflected_ipa, tuple(feats.split(';'))))
                tp = ATP(apply_phonology=True, feature_space=feature_space)
                tp.train(pairs)
                
                suffixes = set()
                for leaf in tp.get_leaves():
                    if leaf.switch_statement.productive:
                        suffix = leaf.switch_statement.default_case.name.split('lemma')[-1].replace(' + ', '')
                        suffixes.add(suffix)
                if 'z' in suffixes and 's' in suffixes:
                    suffixes.discard('z')
                if 't' in suffixes and 'd' in suffixes:
                    suffixes.discard('t')
                for suffix in suffixes:
                    if suffix == 'ɪŋ':
                        ing[i] += 1
                    if suffix in {'d', 't'}:
                        d[i] += 1
                    if suffix in {'s', 'z'}:
                        s[i] += 1

        assert(ing == s == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
        assert(d == [0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])

    def test_inflect_1(self):
        train_pairs = [('finger', 'fingerz', 'PL'), 
              ('block', 'blocks', 'PL'), 
              ('car', 'carz', 'PL'), 
              ('toddler', 'toddlerz', 'PL'),
              ('foot', 'feet', 'PL'),
              ('snack', 'snacks', 'PL'),
              ('catcher', 'catcherz', 'PL'),
              ('carrot', 'carrots', 'PL'),
              
              ('ask', 'askt', 'PST'),
              ('run', 'ran', 'PST'),
              ('walk', 'walkt', 'PST'),
              ('pay', 'payd', 'PST'),
              ('link', 'linkt', 'PST'),
              ('smack', 'smackt', 'PST'),
              ('smell', 'smelld', 'PST'),
              ('think', 'thought', 'PST'),
              ('fight', 'fought', 'PST'),
              ('lay', 'layd', 'PST'),
              ('catch', 'caught', 'PST'),
              ('call', 'calld', 'PST'),
              ('play', 'playd', 'PST'),
              ('look', 'lookd', 'PST')]
        tp = ATP(apply_phonology=False, feature_space={'PL', 'PST'})
        tp.train(train_pairs)
        for leaf in tp.get_leaves():
            if leaf.switch_statement.productive:
                best_case = leaf.switch_statement.default_case
            elif leaf.switch_statement.get_closest_to_productive():
                best_case = leaf.switch_statement.get_closest_to_productive()

        c = 0
        t = 0
        for lemma, inflected, feats in train_pairs:
            pred = tp.inflect(lemma, feats)
            if pred == inflected:
                c += 1
            t += 1
        assert(c / t == 1.0)

        test_pairs = [('walker', 'walkerz', 'PL'), 
              ('feeler', 'feelerz', 'PL'), 
              ('plank', 'planks', 'PL'), 
              ('peanut', 'peanuts', 'PL'),
              
              ('talk', 'talkt', 'PST'),
              ('hurl', 'hurld', 'PST'),
              ('glean', 'gleand', 'PST')]

        c = 0
        t = 0
        for lemma, inflected, feats in test_pairs:
            pred = tp.inflect(lemma, feats)
            if pred == inflected:
                c += 1
            t += 1
        assert(c / t == 1.0)
        
if __name__ == "__main__":
    unittest.main()