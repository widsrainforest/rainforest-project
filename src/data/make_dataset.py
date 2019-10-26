# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

import pandas as pd
import numpy as np
from PIL import Image


PARENT_PATH = Path(os.getcwd()).resolve().parents[0]
DATA_PATH = os.path.join(PARENT_PATH, 'data')

def load_raw_labels(): 
    df = pd.read_csv(os.path.join(DATA_PATH, 'raw','train_v2.csv'))

    return df

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

def save_data(df, path, filename):

    df.to_csv(os.path.join(DATA_PATH, path, filename), index=False)

def make_binary_labels(df):
    '''
        Input: df from train_v2.csv, Ouput: df with binary values for each possible label.
    '''
    unique_labels = []

    for string in df["tags"]:
        labels = string.split(' ')
        for label in labels:
            if label not in unique_labels:
                unique_labels.append(label)

    label_map = {label:i for i, label in enumerate(unique_labels)}
    y = []
    n = len(unique_labels)

    for tag in df.tags:
        row_labels = np.zeros(n)
        for label in tag.split(' '):
            row_labels[label_map[label]] = 1
            
        y.append(row_labels)

    y = np.array(y, np.uint8)
    df_y = pd.DataFrame(y, columns=unique_labels)

    with open(os.path.join(DATA_PATH, 'processed','labels_list.txt'), 'w') as f:
        json.dump(unique_labels, f)

    return pd.concat([df, df_y], axis=1)

def load_raw_jpgs():
    image_path = os.path.join(DATA_PATH, 'raw', 'train-jpg')
    image_arrays = []
    filenames = []

    for i, filename in enumerate(os.listdir(image_path)):
        filenames.append(filename[:-4]) # Remove '.jpg'
        with Image.open(os.path.join(image_path, filename)) as temp_file:
            image_arrays.append(np.array(temp_file)[:,:,:3])

    return pd.DataFrame.from_dict({'image_name':filenames, 'pixel_array':image_arrays})

def save_interim_images(df):
    df.to_csv(os.path.join(DATA_PATH, 'interim','interim_images.csv'), index=False)

def make_processed_data(df_images, df_labels):
    '''
        Input: Interim images DataFrame
        Output: Prcessed DataFrame (mean, min, and max pixel values)
    '''

    processed_data = pd.DataFrame(df_images.image_name)

    r_mean = []
    g_mean = []
    b_mean = []

    r_max = []
    g_max = []
    b_max = []    

    r_min = []
    g_min = []
    b_min = []

    for image_array in df_images.pixel_array:
        r = image_array[:,:,0].ravel()
        g = image_array[:,:,1].ravel()
        b = image_array[:,:,2].ravel()
        
        r_mean.append(np.mean(r))
        g_mean.append(np.mean(g))
        b_mean.append(np.mean(b))

        r_max.append(np.max(r))
        g_max.append(np.max(g))
        b_max.append(np.max(b))     

        r_min.append(np.min(r))
        g_min.append(np.min(g))
        b_min.append(np.min(b))      

    processed_data['r_mean'] = pd.Series(r_mean)
    processed_data['g_mean'] = pd.Series(g_mean)
    processed_data['b_mean'] = pd.Series(b_mean)

    processed_data['r_max'] = pd.Series(r_max)
    processed_data['g_max'] = pd.Series(g_max)
    processed_data['b_max'] = pd.Series(b_max)

    processed_data['r_min'] = pd.Series(r_min)
    processed_data['g_min'] = pd.Series(g_min)
    processed_data['b_min'] = pd.Series(b_min)

    processed_data = processed_data.merge(df_labels, on='image_name')

    return processed_data

def save_processed_data(df):

    with open(os.path.join(DATA_PATH, 'processed','labels_list.txt'), 'r') as f:
        unique_labels = json.load(f)

    y = df[unique_labels].copy()
    y.set_index(df['image_name'], inplace=True)
    y.reset_index(inplace=True)

    df.drop(columns=unique_labels+['tags'], inplace=True)

    df.to_csv(os.path.join(DATA_PATH, 'processed','processed_data_X.csv'), index=False)
    y.to_csv(os.path.join(DATA_PATH, 'processed','processed_labels_Y.csv'), index=False)

def add_random_lat_lon(df, lat_lon):

    mean, cov = [0, 0], [(0, 10), (5, 0)]
    n = len(df)
    data = np.random.multivariate_normal(mean, cov, n)

    lat = data[:,0]
    lon = data[:,1]

    lat = lat + lat_lon[0]
    lon = lon + lat_lon[1]

    df['lat'] = pd.Series(lat)
    df['lon'] = pd.Series(lon)
    
    return df
