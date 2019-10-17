# -*- coding: utf-8 -*-
import os
from pathlib import Path

import pandas as pd
import numpy as np
from PIL import Image


PARENT_PATH = Path(os.getcwd()).resolve().parents[0]
DATA_PATH = os.path.join(PARENT_PATH, 'data')

def load_raw_labels():
    df = pd.read_csv(os.path.join(DATA_PATH, 'raw','train_v2.csv'))
    print("THis is new")
    return df

