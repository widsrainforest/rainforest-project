# -*- coding: utf-8 -*-
import datetime as dt
import json
import os
from pathlib import Path

import pandas as pd
import pickle as pkl
import numpy as np

from sklearn.base import clone
from sklearn.metrics import fbeta_score

PARENT_PATH = Path(os.getcwd()).resolve().parents[0]
DATA_PATH = os.path.join(PARENT_PATH, 'data')

def load_independent_vars():
    df = pd.read_csv(os.path.join(DATA_PATH, 'processed','processed_data_X.csv'))
    df.drop('image_name', axis=1, inplace=True)

    return df

def load_dependent_vars():
    df = pd.read_csv(os.path.join(DATA_PATH, 'processed','processed_labels_Y.csv'))
    df.drop('image_name', axis=1, inplace=True)

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

def train_multi_labels(model, X, Y, split='fixed'):
    '''
        Inputs:
            split='fixed', set the train/test split to 0.8 of the data
    '''
    X.drop(columns=['image_name'], inplace=True)
    Y.drop(columns=['image_name'], inplace=True)

    labels = load_labels()

    f2_scores = []
    models = []

    for label in labels:
        model_copy = clone(model)
        
        y = Y[label]

        temp_model, f2_score = train_score_model(model_copy, X, y, split)
        f2_scores.append(f2_score)
        models.append(temp_model)
        
        print(label, f2_score)

    print('\n***********\n')
    print('Mean f2 score: ', np.mean(f2_scores))

    models = dict(zip(labels, models))
    labels.insert(0, 'mean')
    f2_scores.insert(0, np.mean(f2_scores))
    f2_scores = dict(zip(labels, f2_scores))

    return models, f2_scores

def save_models_scores(models, scores, model_name):
    '''
        Inputs:
            models, dictionary with keys = labels, values = trained model
            scores, dictionary with keys = lables, values = f2 score
            model_name, string of name that will be saved

        Outputs:
            None, saves pickle files of models and csv file of scores
    '''
    today = dt.datetime.now()
    today = today.strftime('%d_%b_%y')

    model_path = os.path.join(PARENT_PATH, 'models', today+'_'+model_name)

    if not os.path.isdir(model_path):
        os.mkdir(model_path)

    f2_df = pd.DataFrame.from_dict({'label':list(scores.keys()), 
                                    'f2_score':list(scores.values())})
    f2_df.to_csv(os.path.join(model_path, today+'_f2score.csv'), index=False)

    for key in models.keys():
        filename = os.path.join(model_path, key+'.pkl')

        with open(filename, 'wb') as f:
            pkl.dump(models[key], f)