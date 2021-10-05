# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 13:11:22 2021

@author: Liam

Converts from STK UTCG -> python datetime and vice versa
"""

import datetime

def datetime2UTCG(dt):
    return dt.strftime("%d %b %Y %H:%M:%S.%f")

def UTCG2datetime(date_string):
    return datetime.datetime.strptime(date_string[:-5], "%d %b %Y %H:%M:%S.%f")

#example_UTCG = '1 Jul 2020 16:00:00.000 UTCG'

#x = datetime.datetime.now()

#y = UTCG2datetime(example_UTCG)

#print(y)