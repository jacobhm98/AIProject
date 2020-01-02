# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 14:29:31 2019

@author: Oscar
"""
from Prediction import Prediction
import array as arr

pred = Prediction()
a = arr.array('d')
b = arr.array('d')
a, b, c, d, e = pred.inference("GOOGL", 15000, 30, 3)
print(a[0], b[0], c, d, e)

s = pred.stockprices("GOOGL", 10)
print(s)