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
a, b, c, d = pred.predict("2016/01/01", "2019/11/06")
print(a[0], b, c, d)