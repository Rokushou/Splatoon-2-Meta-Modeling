'''LOAD'''
# %load /Users/rokushou/Desktop/header.py
'''GENERAL'''
import os
#import time
#import timeit
#import warnings
#warnings.simplefilter('ignore')
import random
import collections
#import secrets
import math
import itertools
'''DATA'''
import numpy as np
import pandas as pd
# import databricks.koalas as ks
'''MONGO'''
#from pymongo import MongoClient
'''PLOT'''
import matplotlib.pyplot as plt
plt.style.use('seaborn-pastel')
font = {'size':16}
import seaborn as sns
'''SCIPY/STATS'''
#import scipy.stats as scs
from scipy.optimize import nnls
#import statsmodels.api as sm
'''SCIKIT LEARN'''
#from sklearn.datasets import make_classification, load_iris, load_boston, load_digits
#from sklearn.pipeline import Pipeline
#from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split, KFold, ShuffleSplit, cross_val_score, GridSearchCV, cross_val_predict
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, r2_score, mean_squared_error, classification_report, make_scorer
#from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
#from sklearn.linear_model import LinearRegression, LogisticRegression
#from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor, GradientBoostingClassifier, AdaBoostRegressor, AdaBoostClassifier
from sklearn.decomposition import PCA, NMF
from sklearn.cluster import KMeans
#from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
'''TENSORFLOW'''
#import tensorflow as tf
'''NLTK'''
#import nltk
#import unicodedata
#import string
#from nltk.corpus import stopwords
#from nltk.tokenize import sent_tokenize, word_tokenize
#from nltk.stem.porter import PorterStemmer
#from nltk.stem.snowball import SnowballStemmer
#from nltk.stem.wordnet import WordNetLemmatizer
'''NETWORK'''
import networkx as nx
import nxpd
import community as comm
'''FUNCTIONS'''
nrange = lambda x : itertools.repeat(None, x)
def argpsort(a, k):
    return np.argpartition(a, range(k))[:k]
def arghsort(a, k):
    b = np.argpartition(a, k)[:k]
    return b[np.argsort(a[b])]
'''PALETTE'''
t = 'setsuna'
qan = {'setsuna':'quanta'}
twi = '#DCB8E7' #Pale, light grayish mulberry
twi_blu = '#273873' #Dark sapphire blue
twi_pur = '#662D8A' #Moderate purple
twi_pnk = '#ED438D' #Brilliant raspberry
'''RETURN'''
!fortune | cowsay -f dragon
