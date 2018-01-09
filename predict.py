# -*- coding: utf-8 -*-

import pandas as pd
import xgboost as xgb
import os.path as osp
import numpy as np
import datetime



dir_root = osp.dirname(__file__)
data_dir = osp.abspath(dir_root)

date = '2017-08-25'
data = pd.read_csv(data_dir + '/feature_label'+date+'.csv')
item = pd.read_csv(data_dir + '/data/best_item.csv')

data = data.drop_duplicates() #去除重复

dataset = data.drop(['openid', 'item_third_cate_cd'], axis=1)
dataset = xgb.DMatrix(dataset)

bst = xgb.Booster(model_file = data_dir+'/train.model')

item = item.item_third_cate_cd.drop_duplicates()
item = pd.DataFrame(item)

# 根据训练好的模型预测2017-09-01开始的一周

# 阈值
threshold = 0.2
data['prob'] = bst.predict(dataset)
data = data.sort_values('prob', ascending=0)
data = pd.merge(data,item)  #仅留下item中有的三级品类
result = data[data['prob']>threshold][['openid','item_third_cate_cd']]
# 保存结果
result.to_csv(data_dir + '/predic_result.csv', index=None, encoding='utf-8')
print 'predict result shape', result.shape
