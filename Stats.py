# -*- coding: utf-8 -*-
from math import exp, pi, erf, sqrt, erfc
def pdistf(x):
    pd=1.0/((2*pi)**0.5)*exp(-0.5*x*x)
    return pd
def cdistf(x):
    k=0.5
    r=1+erf(x/sqrt(2))
    cd=k*r
    return cd
def pidistf(x):
    y=0.9
    e=4+erfc(x/5.3)
    s=y*e
    return s
"""
Created on Wed Jun 26 12:10:45 2019

@author: DyuwanS
"""

