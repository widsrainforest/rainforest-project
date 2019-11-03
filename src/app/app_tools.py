# -*- coding: utf-8 -*-
import numpy as np
import os
from pathlib import Path
import pickle as pkl
import sys

from PIL import Image

sys.path.append("..")

from src.data import make_dataset

PARENT_PATH = Path(os.getcwd()).resolve().parents[0]
DATA_PATH = os.path.join(PARENT_PATH, 'data')
MODELS_PATH = os.path.join(PARENT_PATH, 'models')
IMAGES = make_dataset.load_raw_jpgs()

def load_models(model_folder):
    model_path = os.path.join(MODELS_PATH, model_folder)

    pkl_files = [f for f in os.listdir(model_path) if '.pkl' in f]

    models = []
    labels = []

    for filename in pkl_files:
        with open(os.path.join(model_path, filename), 'rb') as pkl_f:
            models.append(pkl.load(pkl_f))
            labels.append(filename[:-4])

    return models, labels

def load_image(filename):
    image_path = os.path.join(DATA_PATH, 'raw', 'train-jpg')

    with Image.open(os.path.join(image_path, filename)) as temp_file:
        
        image_array = np.array(temp_file)[:,:,:3]

    return image_array

def make_features(image_array):
        r = image_array[:,:,0].ravel()
        g = image_array[:,:,1].ravel()
        b = image_array[:,:,2].ravel()
        
        features = []
        features.append(np.mean(r))
        features.append(np.mean(g))
        features.append(np.mean(b))

        features.append(np.max(r))
        features.append(np.max(g))
        features.append(np.max(b))   

        features.append(np.min(r)) 
        features.append(np.min(b))
        features.append(np.min(g)) 

        return np.array(features)

def load_predict_image(filename, models):
    image_array = load_image(filename)

    X = make_features(image_array)

    Y = []

    for model in models:
        Y.append(model.predict(X.reshape(1, -1))[0])

    return Y