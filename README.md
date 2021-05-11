# ATP-morphology

_The Greedy and Recursive Search for Morphological Productivity_<br>
Caleb Belth, Sarah Payne, Deniz Beser, Jordan Kodner, Charles Yang<br>
CogSci, 2021

If used, please cite:
```bibtex
bibtex coming soon
```

## Setup

```bash
$ git clone git@github.com:cbelth/ATP-morphology.git
$ cd ATP-morphology
$ python setup.py
```

To test the setup, run
```bash
$ cd test/
$ python tester.py
```

## Example Usage

The following examples assume that they are being run from the `src/` directory.

### Train and Inflect

```python
# import code
>> from atp import ATP
>> from utils import load_german_CHILDES
# load some data
>> pairs, feature_space = load_german_CHILDES()
# initialize an ATP model
>> atp = ATP(feature_space=feature_space)
# train ATP
>> atp.train(pairs)
>> atp.inflect('Sache', ('F',)) # ATP produces the correct inflection
'Sachen'
>> atp.inflect('Gleis', ('N',)) # again for a neuter noun
'Gleise'
```

### Inflect without Features

```python
...
>> atp.inflect_no_feat('Sache', ()) # the result is still correct
'Sachen'
>> atp.inflect_no_feat('Gleis', ())
'Gleise'
>> atp.inflect_no_feat('Kach', ()) # for a nonce word with unknown gender, ATP produces the -er suffix, as do a majority of humans
'Kacher'
```

### Training on New Data

Suppose we have a simple language with just four known lemmas: 'a', 'b', 'c', and 'd,' which oddly can be inflected as either nouns or verbs.

Let's say that nouns are marked with a '-' suffix and verbs with a '+' suffix, with the exception of 'd', which takes '*' as a noun and '**' as a verb.

We can initialize the data as below,

```python
>> pairs = [('a', 'a-', ('Noun',)), 
            ('b', 'b-', ('Noun',)), 
            ('c', 'c-', ('Noun',)),
            ('d', 'd*', ('Noun',)),
            ('a', 'a+', ('Verb',)),
            ('b', 'b+', ('Verb',)),
            ('c', 'c+', ('Verb',)),
            ('d', 'd**', ('Verb',))]
>> feature_space = {'Noun', 'Verb'}
```
and train an ATP model as before,
```python
>> atp = ATP(feature_space)
>> atp.train(pairs)
```
If we then introduce a new lemma 'e', the model that ATP learned correctly inflects it:
```python
>> atp.inflect('e', ('Noun',))
'e-'
>> atp.inflect('e', ('Verb',))
'e+'
```

Moreover, since it has seen the exception 'd' during training, it can still correctly produce it's odd suffixes too:
```python
>> atp.inflect('d', ('Noun',))
'd*'
>> atp.inflect('d', ('Verb',))
'd**'
```

## Replicating Experiments

To replicate the experiments, see the Jupyter notebook at `notebooks/Experiments.ipynb`.