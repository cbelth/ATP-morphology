import os
import sys
import argparse
from collections import defaultdict

from utils import load_pairs, most_freq, tolerance_principle, hamming_distance
from tp_switch_statement import TPSwitchStatement
from semantic_condition import SemanticCondition
from phonological_condition import PhonologicalCondition

NEG_SYMBOL = '¬'

class ATP:
    def __init__(self, feature_space, apply_phonology=False):
        '''
        The main class for ATP.
        '''
        self.feature_space = set(SemanticCondition(op) for op in feature_space)
        self.apply_phonology = apply_phonology # see tp_switch_statement.py for a description of this paramter. You should pretty much never need to set it to True.

    class Node:
        '''
        A node in a decision tree.
        '''
        def __init__(self, name, switch_statement=None):
            self.name = name
            self.left_child = None
            self.right_child = None
            self.switch_statement = switch_statement

        def add_child(self, left, branch_condition, child_node):
            '''
            Adds a child to the node.

            :left: if True, add as a left child; otherwise as a right child.
            :branch_condition: a tuple (True/False, split_condition) where the first element is False if the split_condition should be negated.
            :child_node: an ATP.Node object.
            '''
            if left:
                self.left_child = (branch_condition, child_node)
            else:
                self.right_child = (branch_condition, child_node)

        def get_children(self):
            '''
            :return: a tuple of children
            '''
            if self.left_child and self.right_child:
                return (self.left_child, self.right_child)
            elif self.left_child:
                return (self.left_child,)
            elif self.right_child:
                return (self.right_child,)
            return ()

        def num_children(self):
            '''
            :return: the number of children (0, 1, or 2).
            '''
            return len(self.get_children())

    def train(self, pairs):
        '''
        :pairs: pairs to train on 
        '''        
        # build labels
        tp = TPSwitchStatement(apply_phonology=self.apply_phonology, pairs=pairs)
        labels = list()
        for lemma, _, feats in pairs:
            labels.append(tp.get_case(lemma, feats).name)

        # recursivly build the decision tree
        self.root = self.build_node(pairs, labels)

    def accuracy(self, pairs):
        '''
        :pairs: pairs to compute accuracy over
        '''
        c, t = 0, 0
        for lemma, inflected, feats in pairs:
            if self.inflect(lemma, feats) == inflected:
                c += 1
            t += 1
        return c / t if t > 0 else 0

    def guess_inflection(self, lemma, best_node):
        '''
        :lemma: the lemma to inflect
        :best_node: the deepest node logically compatible with the lemma.

        :return: an inflected form using the nearest-neighbor at the :best_node: (using Hamming distance).
        '''
        options = sorted(best_node.switch_statement.vocab, key=lambda it: hamming_distance(lemma, it[0]))
        closest_lemma, closest_inflected = options[0][:-1]
        suffix_of_closest = closest_inflected[len(closest_lemma):]
        return f'{lemma}{suffix_of_closest}'

    def inflect(self, lemma, features, return_whether_guess=False):
        '''
        Inflect a lemma. Performs a depth-first search to the leaf with the correct switch statement.

        :lemma: the lemma to inflect
        :features: the features specifying which inflection to produce
        :return_whether_guess: if True, it will also return a boolean specifying whether guessing was required
        '''
        frontier = [self.root]
        while len(frontier) != 0:
            node = frontier.pop()
            if node.num_children() == 0:
                # if there is a productive process apply it. Or if the (lemma, features) was memorized.
                if node.switch_statement.productive or node.switch_statement.memorized(lemma, features):
                    pred = node.switch_statement.inflect(lemma, features)
                    if return_whether_guess:
                        return pred, False
                    return pred
                else: # otherwise guess an inflection
                    guess = self.guess_inflection(lemma, node)
                    if return_whether_guess:
                        return guess, True
                    return guess
            else:
                for child_branch_condition, child in node.get_children():
                    pos, condition = child_branch_condition
                    if (pos and condition.applies(lemma, features)) or (not pos and not condition.applies(lemma, features)):
                        frontier.append(child)
        print('*** ERROR ***')

    def inflect_no_feat(self, lemma, features, return_whether_guess=False):
        '''
        Inflect a lemma while ignoring a particular feature (i.e., allowing the features to contain any of that features values).
        This was implemented for allowing German words with unkown gender to be inflected on a model trained with gender.

        :lemma: the lemma to inflect
        :features: the features specifying which inflection to produce
        :vals_of_feat: 
        :return_whether_guess: if True, it will also return a boolean specifying whether guessing was required
        '''
        frontier = [self.root]
        valid_leaves = list()
        while len(frontier) != 0:
            node = frontier.pop()
            if node.num_children() == 0:
                valid_leaves.append(node)
            else:
                for child_branch_condition, child in node.get_children():
                    pos, condition = child_branch_condition
                    if condition.condition_type == 'Semantic' or (pos and condition.applies(lemma, features)) or (not pos and not condition.applies(lemma, features)):
                        frontier.append(child)
        # choose a node
        node = None
        valid_productive_leaves = list(filter(lambda it: not it.name.endswith('No Productive Process'), valid_leaves))
        if len(valid_leaves) == 1:
            node = valid_leaves[0]
        elif len(valid_productive_leaves) == 1:
            node = valid_productive_leaves[0]
        elif len(valid_productive_leaves) > 0:
            # get deepest node
            node = sorted(valid_productive_leaves, reverse=True, key=lambda it: (it.name.count(','), len(it.switch_statement.vocab)))[0]
        else:
            assert(len(valid_productive_leaves) == 0)
            # get deepest node
            node = sorted(valid_leaves, reverse=True, key=lambda it: (it.name.count(','), len(it.switch_statement.vocab)))[0]

        if node.switch_statement.productive or node.switch_statement.memorized(lemma, features):
            pred = node.switch_statement.inflect(lemma, features)
            if return_whether_guess:
                return pred, False
            return pred
        else:
            guess = self.guess_inflection(lemma, node)
            if return_whether_guess:
                return guess, True
            return guess

    def get_leaves(self):
        '''
        :return: the leaf nodes of the tree.
        '''
        leaves = list()
        frontier = [self.root]
        while len(frontier) != 0:
            node = frontier.pop()
            if node.num_children() == 0:
                leaves.append(node)
            else:
                for _, child in node.get_children():
                    frontier.append(child)
        return leaves

    def build_node(self, _pairs, _labels, split_options=None, path_string=''):
        '''
        A recursive method builds a node to grow a decision tree.

        :_pairs: training pairs.
        :labels: the "labels" (effectively suffixes) of the training pairs.
        :split_options: features options for splitting on.
        :path_string: a string denoting the path taken so far.
        '''
        if split_options == None:
            split_options = set(self.feature_space)
        lemma_ending_options = self.phonological_features(_pairs, _labels)
        _names = set(it.name for it in split_options)
        split_options.update(filter(lambda it: it.name not in _names, lemma_ending_options))
        split_options.difference_update(self.get_useless_splits(split_options, _pairs, _labels))

        # check if productive
        tp = TPSwitchStatement(apply_phonology=self.apply_phonology, pairs=_pairs)
        productive = tp.get_productive()
        if productive: # productive
            assert(tp.productive)
            tp.default_case = productive
            tp.cases.remove(productive)
            return ATP.Node(f'{path_string} => {productive.name}', tp)
        elif len(split_options) == 0: # productive, but no features left
            return ATP.Node(f'{path_string} => No Productive Process', tp)

        # maximize productivity via consistency
        split_feature, splits, splits_labels = self.maximize_productivity(_pairs, _labels, split_options)
        # create a new node
        node = ATP.Node(f'{path_string}', None)
        assert(len(splits.keys()) == 2)

        split_feature_name = f'{split_feature}'
        neg_split_feature_name = f'{NEG_SYMBOL}{split_feature}'

        path = f'{path_string},' if path_string != '' else ''

        # recursively search over the pairs that have the split feature
        node.add_child(left=True, branch_condition=(True, split_feature), child_node=self.build_node(_pairs=splits[split_feature_name], 
                                                                                                     _labels=splits_labels[split_feature_name], 
                                                                                                     split_options=split_options.difference({split_feature}),
                                                                                                     path_string=f'{path}{split_feature_name}'))
        # recursively search over the pairs that do NOT have the split feature
        node.add_child(left=False, branch_condition=(False, split_feature), child_node=self.build_node(_pairs=splits[neg_split_feature_name], 
                                                                                                       _labels=splits_labels[neg_split_feature_name], 
                                                                                                       split_options=split_options.difference({split_feature}),
                                                                                                       path_string=f'{path}{neg_split_feature_name}'))
        return node

    def get_useless_splits(self, options, _pairs, _labels):
        '''
        :return: any split options that are totally uninformative (i.e., all :_pairs: go down the same branch).
        '''
        useless = set()
        for sf in options:
            _, _, splits_labels = self.split(_pairs, _labels, sf)
            subset_labels = splits_labels[sf.name]
            if len(subset_labels) == 0 or len(subset_labels) == len(_labels):
                useless.add(sf)
        return useless

    def phonological_features(self, _pairs, _labels):
        '''
        Add phonological features (lemma endings).

        :_pairs: the training pairs that made it to this node
        :_labels: the training suffixes corresponding to the pairs

        :return: a set of phonological conditions
        '''
        phonological_conditions = set()
        suffix_to_pairs = defaultdict(set)
        ending_to_pairs = defaultdict(set)
        for pair in _pairs:
            lemma, inflected, _ = pair
            if inflected.startswith(lemma):
                suffix = inflected[len(lemma):]
                suffix_to_pairs[suffix].add(pair)
            for ending_length in range(1, 6):
                if len(lemma) > ending_length:
                    ending_to_pairs[lemma[-ending_length:]].add(pair)
        
        skip = set()
        passed_endings = list()
        for suffix, pairs_with_suffix in sorted(suffix_to_pairs.items(), reverse=True, key=lambda it: len(it[1])):
            suffix_passed_endings = list()
            c_total = 0 # counts the pairs at this node that are covered by these ending -> suffix rules
            n_total = 0
            local_skip = set()
            for ending in sorted(list(ending_to_pairs.keys()), key=lambda it: (len(it), it)):
                if any(ending.endswith(e) for e in skip.union(local_skip)):
                    continue
                n = len(ending_to_pairs[ending]) # words with ending
                c = len(pairs_with_suffix.intersection(ending_to_pairs[ending])) # words with ending and suffix
                if tolerance_principle(n=n, c=c):
                    suffix_passed_endings.append(ending)
                    local_skip.add(ending)
                    n_total += n
                    c_total += c
            if len(suffix_passed_endings) > 0:
                n = n_total # words with any of the endings
                c = c_total # words with any of the endings and the suffix
                if tolerance_principle(n=n, c=c) and tolerance_principle(n=len(pairs_with_suffix), c=c):
                    skip.update(suffix_passed_endings)
                    if len(suffix_passed_endings) > 1:
                        suffix_passed_endings = tuple(e for e in suffix_passed_endings)
                    else:
                        suffix_passed_endings = suffix_passed_endings[0]
                    passed_endings.append(suffix_passed_endings)

        for ending in passed_endings:
            phonological_conditions.add(PhonologicalCondition(ending))
        return phonological_conditions

    def consistency(self, _labels):
        '''
        :return: the relative frequency of the most frequent suffix in :_labels:
        '''
        most_frequent_label = most_freq(_labels)
        n = len(_labels)
        c = _labels.count(most_frequent_label) # the frequency of the most frequent suffix
        if c == n == 0:
            return 0
        return c / n

    def maximize_productivity(self, _pairs, _labels, split_options):
        '''
        Perform the split that Maximizes Productivit via consistency, i.e., "the relative frequency of the most frequent suffix that the instances with that feature take."
        '''
        arg_max = None
        max_val = -100000
        for split_feature in split_options:
            _, splits_vals, splits_labels = self.split(_pairs, _labels, split_feature)
            subset_labels = splits_labels[f'{split_feature}']
            consistency = self.consistency(subset_labels)
            if consistency > max_val:
                max_val = consistency
                arg_max = split_feature
            neg_split_feature = f'{NEG_SYMBOL}{split_feature}'
            subset_labels = splits_labels[neg_split_feature]
            consistency = self.consistency(subset_labels)
            if consistency > max_val:
                max_val = consistency
                arg_max = split_feature
        split_feature = arg_max
        return self.split(_pairs, _labels, split_feature)

    def split(self, _pairs, _labels, split_feature):
        '''
        :_pairs: the pairs to split
        :_labels: the :_pairs:' labels

        :return: the :split_feature: a dict mapping the feature/neg-feature to the set of pairs with/without the feature, and a dict doing the same for the labels
        '''
        X = list() # X_s
        X_labels = list()
        Y = list() # X \ X_s
        Y_labels = list()
        for i, pair in enumerate(_pairs):
            lemma, _, feats = pair
            if split_feature.applies(lemma, feats):
                X.append(pair)
                X_labels.append(_labels[i])
            else:
                Y.append(pair)
                Y_labels.append(_labels[i])
        X_name = f'{split_feature}'
        Y_name = f'{NEG_SYMBOL}{split_feature}'
        # a map from left/right subset names to the left/right subsets
        splits = {X_name: X, Y_name: Y}
        # a map from left/right subset names to the left/right subset labels
        splits_labels = {X_name: X_labels, Y_name: Y_labels}
        return split_feature, splits, splits_labels

    def plot_tree(self, save_path, open_pdf=False):
        '''
        A function to plot the decision tree.

        NOTE: in addition to the graphviz python package, this also depends on having Graphviz 
        installed (https://graphviz.org/), which is not automatically installed with the python package.
        Since the import is within this method, everything else should run if you do not wish to go through
        the installation, but you will not be able to visualize trees.

        :save_path: the location to save the tree (it will save as a .pdf)
        '''
        from graphviz import Digraph

        dot = Digraph()
        edges = list()

        frontier = [self.root]
        i = 0
        node_to_name = {self.root.name: f"{self.root.name.split(',')[-1]}--root"}
        while len(frontier) != 0:
            node = frontier.pop()
            dot.attr('node', shape='circle')
            if node.name not in node_to_name:
                node_to_name[node.name] = f'{i}'
                i += 1
            node_name = node_to_name[node.name]
            if node.num_children() > 0:
                dot.node(node_name, '')
            else:
                 dot.node(node_name, node_name.split('--')[0])
            for _, child in node.get_children():
                frontier.append(child)
                if child.name not in node_to_name:
                    if child.num_children() == 0: # leaf node
                        rule_name = child.name.split("=> ")[-1].replace('inflected = lemma', '')
                        if rule_name == ' + ':
                            rule_name = '-∅'
                        if rule_name.startswith(' + '):
                            rule_name = rule_name.replace(' + ', '-')
                        node_to_name[child.name] = f'{rule_name}--{i}'.replace('No Productive Process', 'failed')
                    else:
                        split_feat = child.name.split(',')[-1]
                        node_to_name[child.name] = f'{split_feat}--{i}'
                    i += 1
                child_name = node_to_name[child.name]
                pred = child.name.split(' => ')[0].split(',')[-1]
                edges.append((node_name, pred, child_name))

        for edge in edges:
            dot.edge(edge[0], edge[2], label=f' {edge[1]}')
        
        dot.render(save_path, view=False)

        if open_pdf:
            import subprocess
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, f'{save_path}.pdf'])

def main(args):
    '''
    A function for running from the command line.
    '''
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    pairs, feature_space = load_pairs(args.input, sep=args.sep, feat_sep=args.feat_sep)
    atp = ATP(feature_space=feature_space)
    atp.train(pairs) # train ATP

    if args.test_path: # test ATP if a test path was provided
        pairs, _ = load_pairs(args.test_path, sep=args.sep, feat_sep=args.feat_sep, skip_header=args.skip_header)
        with open(args.out_path, 'w') if args.out_path else sys.stdout as f:
            for lemma, _, feats in pairs:
                f.write(f'{atp.inflect(lemma, feats)}\n')

def parse_args():
    def str2bool(v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True, help="A path to a dataset of training pairs.")
    parser.add_argument('--test_path', '-t', type=str, required=False, default=None, help="A path to a dataset of test pairs.")
    parser.add_argument('--out_path', '-o', type=str, required=False, default=None, help="A path to write the test results to. If None, it will print to stdout.")
    parser.add_argument('--sep', '-s', type=str, required=False, default='\t', help="The column seperator for the input file.")
    parser.add_argument('--feat_sep', '-fs', type=str, required=False, default=';', help="The seperator for features in the input file.")
    parser.add_argument('--skip_header', '-sh', type=str2bool, required=False, default=False, help="If True, skips the first line of the input file, treating it as a header.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args)