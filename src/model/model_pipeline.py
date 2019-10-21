# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.metrics import fbeta_score

PARENT_PATH = Path(os.getcwd()).resolve().parents[0]
DATA_PATH = os.path.join(PARENT_PATH, 'data')

def load_independent_vars():
    df = pd.read_csv(os.path.join(DATA_PATH, 'processed','processed_data_X.csv'))

    return df

def load_dependent_vars():
    df = pd.read_csv(os.path.join(DATA_PATH, 'processed','processed_labels_Y.csv'))

    return df

def load_labels():
    with open(os.path.join(DATA_PATH, 'processed','labels_list.txt'), 'r') as f:
        labels = json.load(f)

    return labels

def train_score_model(model, X, y, split='fixed'):
    '''
        Inputs:
            split='fixed', set the train/test split to 0.8 of the data
    '''
    if split=='fixed':
        split = int(len(X)*.8)
    else:
        raise Exception('split argument not implemented for value other than "fixed."')
    
    X = np.array(X)
    X_train = X[:split]
    X_test = X[split:]

    y = np.array(y)
    y_train = y[:split]
    y_test = y[split:]
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    f2_score = fbeta_score(y_test, y_pred, average='binary', beta=2)

    return model, f2_score