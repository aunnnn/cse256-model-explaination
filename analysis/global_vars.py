
import os
from analysis.misc import renamed_load

from sklearn.feature_extraction.text import TfidfVectorizer


fv = None
clf = None

fv_text_preprocessor = None
fv_text_tokenize = None

feature_names = None
feature_names_set = None
clf_coefficients = None
clf_intercept = None

class GLOBAL_UI_STYLES:
    POSITIVE_COLOR_CLASSNAME = 'blue'
    NEGATIVE_COLOR_CLASSNAME = 'red'

def load_pickle(name):
    with open(name, 'rb') as fin:
        data = renamed_load(fin)
        print("Loaded: ", name)
        return data


def initialize_global_vars():
    global fv, clf, fv_text_tokenize, fv_text_preprocessor
    global feature_names, feature_names_set, clf_coefficients, clf_intercept

    root_dir = os.getcwd()

    fv = load_pickle(os.path.join(root_dir, 'assets/model/fv.pkl'))
    clf = load_pickle(os.path.join(root_dir, 'assets/model/clf.pkl'))

    fv_text_preprocessor = fv.build_preprocessor()
    fv_text_tokenize = fv.build_tokenizer()

    feature_names = fv.get_feature_names()
    feature_names_set = set(feature_names)
    clf_coefficients = clf.coef_[0] # 1d array
    clf_intercept = clf.intercept_[0] # scalar