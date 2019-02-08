# MAS NLP module
# Special utilities that it currently contains:
# -
# -
# -
# -
#
# Credits/Licensing requirements:
#
# This python script uses parts of WordNet
# below you'll find their license
#
### WordNet
#
# License: https://wordnet.princeton.edu/wordnet/license/
#
# Required citation
# Princeton University "About WordNet." WordNet. Princeton University. 2010. <http://wordnet.princeton.edu>
#
# Changes done:
# Added some words to the Exceptions Lists since I'm not using the entire WordNet and can't check word
# authenticity, the morphy function is based on the algorithm described in the wordnet code.
#
### NLTK
# stopwords obtained from NLTK (https://github.com/nltk/nltk/blob/develop/LICENSE.txt)
#
### Wikipedia
#
# Contractions gotten from https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
#
### POS Tagger and Averaged Perceptron
#
# Original work can be found here:
# https://github.com/sloria/textblob-aptagger which is licensed under
# the MIT License https://github.com/sloria/textblob-aptagger/blob/dev/LICENSE
# Copyright 2013 Matthew Honnibal
#
# more in detail explanation of how it works can be found at
# https://explosion.ai/blog/part-of-speech-pos-tagger-in-python
#
# minor modifications where made so it works with RenPy
#
# TODO: Need to move the POS Tagger and the averaged perceptron implementation to a python package 
# so the tagger itself can be trained and pickled easily without having to do it through MAS itself.
# Also need to decide if we'll end up moving the other definitions as well to keep the mas_nlp store
# cleaner, and make it some sort of wrapper around the python package 

init 10 python in mas_nlp:

    import inspect
    import os
    import pickle
    import random
    import re
    import string

    from difflib import SequenceMatcher
    from collections import defaultdict

    DEFAULT_PICKLE_DIR = os.path.normcase(renpy.config.basedir + "/pickles/")
    TAGGER_PICKLE = "tagger.pickle"

######
# String utilities
######

    _CONTRACTIONS_DICT = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "daren't": "dare not",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "everyone's": "everyone is",
        "gimme":"give me",
        "gonna":"going to",
        "gotta":"got to",
        "hadn't": "had not",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'll": "he will",
        "he's": "he is",
        "how'd": "how did",
        "how'll": "how will",
        "how's": "how is",
        "I'd": "I would",
        "I'd've": "I would have",
        "I'll": "I will",
        "I'm": "I am",
        "i'm": "i am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it had",
        "it'll": "it will",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "ne'er":"never",
        "o'clock":"of the clock",
        "ol'":"old",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "shouldn't": "should not",
        "so've": "so have",
        "so's": "so is",
        "that'd": "that would",
        "that'll": "that will",
        "there'd": "there had",
        "there's": "there is",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we had",
        "we'll": "we will",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where is",
        "where've": "where have",
        "who'll": "who will",
        "who's": "who is",
        "who've": "who have",
        "why's": "why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "would've": "would have",
        "wouldn't": "would not",
        "you'll": "you will",
        "you're": "you are",
        "you've": "you have",
        "'tis":"it is"
    }

    _CONTRACTIONS_REGEX = re.compile(r'('+'|'.join(_CONTRACTIONS_DICT.keys())+')')
    _ENGLISH_STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
                      "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
                      'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
                      'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
                      'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                      'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
                      'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                      'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                      'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                      'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                      'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
                      'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
                      'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't",
                      'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
                      'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
                      "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


    _STOPWORDS_REGEX = re.compile(r'(?:^|(?<= ))('+'|'.join(_ENGLISH_STOPWORDS)+')(?:(?= )|$)')


    def _contractions_replace(match):
        """
        Helper internal method used to easily replace the specified contraction with the match
        """
        return _CONTRACTIONS_DICT[match.group(0)]


    def expand_contractions(text, regex=_CONTRACTIONS_REGEX):
        """
        Expands contractions found in text
        :param text: the text string to which we'll expand the contractions inside itself
        :param regex: regex to use to find the contractions, should be left to default most of the time
        :return: the text with the contractions expanded
        """
        return regex.sub(_contractions_replace, text)


    def remove_stopwords(text, regex=_STOPWORDS_REGEX):
        """
        Removes the stopwords found in the text
        :param text: the text string that we'll be removing the stopwords from
        :param regex: regex to be used to find the stopwords in the text, should be left to default unless you want to use
            another set of stopwords
        :return: the text without the stopwords
        """
        return regex.sub('',text)


    def strip_punc(s, all=False):
        """
        Removes punctuation from a string.
        :param s: The string.
        :param all: Remove all punctuation. If False, only removes punctuation from
            the ends of the string.
        """
        if all:
            return re.compile('[{0}]'.format(re.escape(string.punctuation))).sub('', s.strip())
        else:
            return s.strip().strip(string.punctuation)


    def calculate_string_distance(first, final):
        """
        Calculates the string "distance"
        :param first: first string to check
        :param final: second string to check
        :return: The ratio found by the SequenceMatcher
        """
        return SequenceMatcher(None, first.lower(), final.lower()).ratio()


    def normalize(line, accepted_chars='abcdefghijklmnopqrstuvwxyz '):
        """
        Return only the subset of chars from accepted_chars.
        This helps keep the  model relatively small by ignoring punctuation,
        infrequenty symbols, etc.
        """
        return [c.lower() for c in line if c.lower() in accepted_chars]


    def ngram(n, l):
        """ Return all n grams from l after normalizing """
        filtered = normalize(l)
        for start in range(0, len(filtered) - n + 1):
            yield ''.join(filtered[start:start + n])


    def pre_process_sentence( sentence):
        """
        pre_process_sentence expands contractions on a sentence and changes the symbol ? so it can be specially processed
        :param sentence: the sentence to pre-process
        :return: the sentence with the modifications
        """
        # expand the contractions
        expanded_sentence = expand_contractions(sentence.lower())
        # remove punctuation
        return strip_punc(expanded_sentence)

######
# Morphy
######

    class Morphy:

        def __init__(self,base_dir=None):

            if base_dir is None:
                base_dir = os.path.dirname(inspect.getfile(self.__class__))
            self.nouns = {}
            with open(os.path.join(base_dir, 'nouns.pickle'), 'rb') as handle:
                self.nouns = pickle.load(handle)
            self.adjs = {}
            with open(os.path.join(base_dir, 'adjs.pickle'), 'rb') as handle:
                self.adjs = pickle.load(handle)
            self.advs = {}
            with open(os.path.join(base_dir, 'advs.pickle'), 'rb') as handle:
                self.advs = pickle.load(handle)
            self.verbs = {}
            with open(os.path.join(base_dir, 'verbs.pickle'), 'rb') as handle:
                self.verbs = pickle.load(handle)
            self.modals = {"would": "will", "should":"shall", "ought":"must", "could":"can"}

        #
        # morphy function based on WordNet morphy function
        # https://wordnet.princeton.edu/man/morphy.7WN.html
        #

        def morphy(self, word, pos_tag=None):
            """
            morphy function transforms word into it's base form for easier processing
            :param word: word to transform
            :param pos_tag: part of speech tag of this word, for morphy functions we
                only deal with nouns, adjectives and verbs, for other tags we return
                the word as is. If no tag is specified we'll check in the exceptions
                lists, if it's not in those we return the word as is since there's
                nothing we can do to the word without more info
            :return: the word base form if possible, the word without modifications
                otherwise
            """
            if pos_tag is not None:
                if 'JJ' in pos_tag:
                    # It must be an adjective
                    base = self.adjs.get(word, None)
                    if base is not None:
                        return base
                    # morphy transforms
                    new, changes = re.subn(r'(er)\b', '', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(est)\b', '', word)
                    if changes > 0: return new
                elif 'RB' in pos_tag:
                    # It must be an adverb
                    base = self.advs.get(word, None)
                    if base is not None:
                        return base
                        # No rules applicable to adverbs
                elif 'NN' in pos_tag:
                    # It must be an noun
                    base = self.nouns.get(word, None)
                    if base is not None:
                        return base
                    # morphy transforms for nouns
                    new, changes = re.subn(r'(ses)\b', 's', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(xes)\b', 'x', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(zes)\b', 'z', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(ches)\b', 'ch', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(shes)\b', 'sh', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(men)\b', 'man', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(ies)\b', 'y', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(s)\b', '', word)
                    if changes > 0: return new
                elif 'VB' in pos_tag:
                    # It must be an verb
                    base = self.verbs.get(word, None)
                    if base is not None:
                        return base
                    new, changes = re.subn(r'(ies)\b', 'y', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(es)\b', '', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(s)\b', '', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(ing)\b', '', word)
                    if changes > 0: return new
                    new, changes = re.subn(r'(ed)\b', '', word)
                    if changes > 0: return new
                elif 'MD' in pos_tag:
                    base =  self.modals.get(word,None)
                    if base is not None:
                        return base
            return word

        def change_to_base(self, words):
            """
            change_to_base An auxiliary method that changes the input list of tuples words to base form if possible
            :param words: list of tuples containing word and tag
            :return: a list of words in their base form
            """
            base_words = []
            for word, tag in words:
                # use morphy to get base form and lowercase each word
                base_word = self.morphy(word, tag)
                base_words.append(base_word)
            return base_words


######
# Averaged Perceptron Class
######

    class AveragedPerceptron(object):

        """
        An averaged perceptron, as implemented by Matthew Honnibal.
        See more implementation details here:
            http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/
        """

        def __init__(self):
            # Each feature gets its own weight vector, so weights is a dict-of-dicts
            self.weights = {}
            self.classes = set()
            # The accumulated values, for the averaging. These will be keyed by
            # feature/class tuples
            self._totals = defaultdict(int)
            # The last time the feature was changed, for the averaging. Also
            # keyed by feature/class tuples
            # (tstamps is short for timestamps)
            self._tstamps = defaultdict(int)
            # Number of instances seen
            self.i = 0

        def predict(self, features):
            """
            Dot-product the features and current weights and return the best label.
            """
            scores = defaultdict(float)
            for feat, value in features.items():
                if feat not in self.weights or value == 0:
                    continue
                weights = self.weights[feat]
                for label, weight in weights.items():
                    scores[label] += value * weight
            # Do a secondary alphabetic sort, for stability
            return max(self.classes, key=lambda label: (scores[label], label))

        def update(self, truth, guess, features):
            """
            Update the feature weights.
            """
            def upd_feat(c, f, w, v):
                param = (f, c)
                self._totals[param] += (self.i - self._tstamps[param]) * w
                self._tstamps[param] = self.i
                self.weights[f][c] = w + v

            self.i += 1
            if truth == guess:
                return None
            for f in features:
                weights = self.weights.setdefault(f, {})
                upd_feat(truth, f, weights.get(truth, 0.0), 1.0)
                upd_feat(guess, f, weights.get(guess, 0.0), -1.0)
            return None

        def average_weights(self):
            """
            Average weights from all iterations.
            """
            for feat, weights in self.weights.items():
                new_feat_weights = {}
                for clas, weight in weights.items():
                    param = (feat, clas)
                    total = self._totals[param]
                    total += (self.i - self._tstamps[param]) * weight
                    averaged = round(total / float(self.i), 3)
                    if averaged:
                        new_feat_weights[clas] = averaged
                self.weights[feat] = new_feat_weights
            return None

        def save(self, path):
            """
            Save the pickled model weights.
            """
            return pickle.dump(dict(self.weights), open(path, 'w'))

        def load(self, path):
            """
            Load the pickled model weights.
            """
            self.weights = pickle.load(open(path))
            return None

    ######
    # POS Tagger
    ######

    class PerceptronTagger():

        """
        Greedy Averaged Perceptron tagger, as implemented by Matthew Honnibal.

        See more implementation details here:
            http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/

        :param load: Load the pickled model upon instantiation.
        """

        START = ['-START-', '-START2-']
        END = ['-END-', '-END2-']

        AP_MODEL_LOC = os.path.join(DEFAULT_PICKLE_DIR, TAGGER_PICKLE)

        def __init__(self, load=False, base_dir=None, pickle=None):
            self.model = AveragedPerceptron()
            self.tagdict = {}
            self.classes = set()
            if load:
                self.load(self.AP_MODEL_LOC if base_dir is None else os.path.join(base_dir, pickle))

        def tag(self, corpus, use_tokens=True):
            """
            Tags a string `corpus`.
            """
            # Assume untokenized corpus has \n between sentences and ' ' between words
            w_split = tokenize if use_tokens else lambda s: s.split()

            def split_sents(corpus):
                yield w_split(corpus)

            prev, prev2 = self.START
            tokens = []
            for words in split_sents(corpus):
                context = self.START + [self._normalize(w) for w in words] + self.END
                for i, word in enumerate(words):
                    tag = self.tagdict.get(word)
                    if not tag:
                        features = self._get_features(i, word, context, prev, prev2)
                        tag = self.model.predict(features)
                    tokens.append((word, tag))
                    prev2 = prev
                    prev = tag
            return tokens

        def train(self, sentences, save_loc=None, nr_iter=5):
            """
            Train a model from sentences, and save it at ``save_loc``. ``nr_iter``
            controls the number of Perceptron training iterations.

            :param sentences: A list of (words, tags) tuples.
            :param save_loc: If not ``None``, saves a pickled model in this location.
            :param nr_iter: Number of training iterations.
            """
            self._make_tagdict(sentences)
            self.model.classes = self.classes
            for iter_ in range(nr_iter):
                c = 0
                n = 0
                for words, tags in sentences:
                    prev, prev2 = self.START
                    context = self.START + [self._normalize(w) for w in words] \
                                                                        + self.END
                    for i, word in enumerate(words):
                        guess = self.tagdict.get(word)
                        if not guess:
                            feats = self._get_features(i, word, context, prev, prev2)
                            guess = self.model.predict(feats)
                            self.model.update(tags[i], guess, feats)
                        prev2 = prev
                        prev = guess
                        c += guess == tags[i]
                        n += 1
                random.shuffle(sentences)
            self.model.average_weights()
            # Pickle as a binary file
            if save_loc is not None:
                pickle.dump((self.model.weights, self.tagdict, self.classes),
                             open(save_loc, 'wb'), -1)
            return None

        def load(self, loc):
            """
            Load a pickled model.
            """
            try:
                w_td_c = pickle.load(open(loc, 'rb'))
            except IOError:
                msg = ("Missing trontagger.pickle file.")
                raise Exception(msg)
            self.model.weights, self.tagdict, self.classes = w_td_c
            self.model.classes = self.classes
            return None

        def _normalize(self, word):
            """
            Normalization used in pre-processing.

            - All words are lower cased
            - Digits in the range 1800-2100 are represented as !YEAR;
            - Other digits are represented as !DIGITS

            :rtype: str
            """
            if '-' in word and word[0] != '-':
                return '!HYPHEN'
            elif word.isdigit() and len(word) == 4:
                return '!YEAR'
            elif word[0].isdigit():
                return '!DIGITS'
            else:
                return word.lower()

        def _get_features(self, i, word, context, prev, prev2):
            """
            Map tokens into a feature representation, implemented as a
            {hashable: float} dict. If the features change, a new model must be
            trained.
            """
            def add(name, *args):
                features[' '.join((name,) + tuple(args))] += 1

            i += len(self.START)
            features = defaultdict(int)
            # It's useful to have a constant feature, which acts sort of like a prior
            add('bias')
            add('i suffix', word[-3:])
            add('i pref1', word[0])
            add('i-1 tag', prev)
            add('i-2 tag', prev2)
            add('i tag+i-2 tag', prev, prev2)
            add('i word', context[i])
            add('i-1 tag+i word', prev, context[i])
            add('i-1 word', context[i-1])
            add('i-1 suffix', context[i-1][-3:])
            add('i-2 word', context[i-2])
            add('i+1 word', context[i+1])
            add('i+1 suffix', context[i+1][-3:])
            add('i+2 word', context[i+2])
            return features

        def _make_tagdict(self, sentences):
            """
            Make a tag dictionary for single-tag words.
            """
            counts = defaultdict(lambda: defaultdict(int))
            for words, tags in sentences:
                for word, tag in zip(words, tags):
                    counts[word][tag] += 1
                    self.classes.add(tag)
            freq_thresh = 20
            ambiguity_thresh = 0.97
            for word, tag_freqs in counts.items():
                tag, mode = max(tag_freqs.items(), key=lambda item: item[1])
                n = sum(tag_freqs.values())
                # Don't add rare words to the tag dictionary
                # Only add quite unambiguous words
                if n >= freq_thresh and (float(mode) / n) >= ambiguity_thresh:
                    self.tagdict[word] = tag
