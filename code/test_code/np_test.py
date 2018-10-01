# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 17:07:50 2017

@author: Gary
"""

import numpy as np # 引用套件並縮寫為 np

ironmen = np.array([46, 8, 11, 11, 4, 56]) # 將 list 透過 numpy 的 array 方法進行轉換
print(ironmen) # 看看 ironmen 的外觀
print(type(ironmen)) # 看看 ironmen 的資料結構
articles = ironmen * 30
print(articles)

