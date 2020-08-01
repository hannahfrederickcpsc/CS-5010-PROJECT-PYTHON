#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 09:50:28 2020

@author: seangrace
"""

import pandas as pd

data = pd.read_csv("/Users/seangrace/Documents/Data/complete.txt")
data.head()
data.tail(15)

data = data.loc[:43,]
data.tail()

data = data.rename(columns={"Winner" : "Winner (VA)"})
data.columns

data.to_csv("/Users/seangrace/Documents/Data/complete_cleaned.csv", index=False)
