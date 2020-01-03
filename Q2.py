from __future__ import unicode_literals
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
from nltk import ngrams

import re

import matplotlib.pyplot as plt
import itertools
import pandas as pd
import numpy as np
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.naive_bayes import MultinomialNB

from scipy import sparse


def neg_tag(text):
    """
    Input is string (e.g. I am not happy.)
    Output is string with neg tags (e.g. I am not NEG_happy.)
    """
    transformed = re.sub(
        r"\b(?:never|nothing|nowhere|noone|none|not|haven't|hasn't|hasnt|hadn't|hadnt|can't|cant|couldn't|couldnt"
        r"|shouldn't|shouldnt|won't|wont|wouldn't|wouldnt|don't|dont|doesn't|doesnt|didn't|didnt|isnt|isn't|aren't"
        r"|arent|aint|ain't|hardly|seldom)\b[\w\s]+[^\w\s]",
        lambda match: re.sub(r'(\s+)(\w+)', r'\1NEG_\2', match.group(0)), text, flags=re.IGNORECASE)
    return transformed


def preprocessing_baseline(list_of_sentences):
    """
    Input is list of raw sentences.
    Output is sentences without punctuations.
    Used for preprocessing method B
    """
    processed_sentences = []

    for sent in list_of_sentences:
        processed = [word.lower() for word in sent.split()]
        remove_punc = [re.sub('[^a-zA-Z_]+', '', t) for t in processed]
        processed_sentences.append(remove_punc)

    if len(processed_sentences) == len(list_of_sentences):
        return processed_sentences
    else:
        print('Length of processed is different from input')


def preprocessing_stpwrd_remvl(list_of_sentences):
    """
    Input is list of raw sentences.
    Output is list of processed sentences.
    Used for preprocessing methods S1, S2, S3
    """

    processed_sentences = []

    for sent in list_of_sentences:
        stemmed = [stemmer.stem(word).lower() for word in sent.split() if word.lower() not in stpwrds]
        processed = [re.sub('[^a-zA-Z]+', '', t) for t in stemmed]
        morethan3 = [t for t in processed if len(t) > 3]
        processed_sentences.append(' '.join(morethan3))

    if len(processed_sentences) == len(list_of_sentences):
        return processed_sentences
    else:
        print('Length of processed is different from input')
