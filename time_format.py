# -*- coding: utf-8 -*-

import os.path as osp
import pandas as pd
import numpy as np
import datetime




# 提取文件目录
dir_root = osp.dirname(__file__)
data_dir = osp.abspath(osp.join(dir_root,  'data'))

behavioral = pd.read_csv(data_dir+'/behavioral.csv')

#将形如‘2016-01-01’的字符串转为标准的datetime的格式
def str_to_date(date):
        return datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])) 

#改变时间格式
behavioral.tm = behavioral.tm.apply(str_to_date)
behavioral.to_csv(data_dir+'/behavioral_tm.csv',index = False)