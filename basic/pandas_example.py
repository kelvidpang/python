#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 20:17:16 2017

@author: kelvidpang
"""

import pandas as pd
import numpy as np
import os

raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
        'age': [42, 52, 36, 24, 73],
        'preTestScore': [4, 24, 31, ".", "."],
        'postTestScore': ["25,000", "94,000", 57, 62, 70]}
df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
df


os.getcwd()
os.chdir(r"/Users/kelvidpang/Desktop/python/git/python")

#write to current folder
df.to_csv('./example.csv')

df = pd.read_csv('./example.csv')
df
