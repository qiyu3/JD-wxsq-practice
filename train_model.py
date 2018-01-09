# -*- coding: utf-8 -*-

import pandas as pd
import xgboost as xgb
import os.path as osp
import numpy as np
import datetime



dir_root = osp.dirname(__file__)
data_dir = osp.abspath(dir_root)
datelist = ['2017-07-05','2017-07-12','2017-07-19','2017-07-26','2017-08-02','2017-08-09']
date_val = '2017-08-16'

data = pd.DataFrame()
for date in datelist:
	data_new = pd.read_csv(data_dir + '/feature_label'+date+'.csv')
	data = pd.concat([data, data_new])

data = data.drop(['openid', 'item_third_cate_cd'], axis=1)
data = data.drop_duplicates() #去除重复
data_y = data.label
data_x = data.drop(['label'], axis=1)

data_val = pd.read_csv(data_dir + '/feature_label'+date_val+'.csv')
data_val = data_val.drop(['openid', 'item_third_cate_cd'], axis=1)
data_val = data_val.drop_duplicates() #去除重复
data_val_y = data_val.label
data_val_x = data_val.drop(['label'], axis=1)

dataset = xgb.DMatrix(data_x,label=data_y)
dataset_val = xgb.DMatrix(data_val_x,label=data_val_y)

params={'booster':'gbtree',
               'objective': 'binary:logistic',
               'eval_metric':'auc', 
               'gamma':0.1,
               'min_child_weight':1.1,
               'max_depth':13,
               'lambda':10,
               'subsample':0.8,
               'colsample_bytree':0.8,
               'colsample_bylevel':1,
               'eta': 0.01,
               'tree_method':'exact',
               'seed':0,
               'nthread':16,
               'scale_pos_weight':100,
               'max_delta_step':1
}

def evalerror(preds, dtrain):
    labels = dtrain.get_label()
    threshold = 0.6
    preds = preds > threshold
    precise = float(sum(labels*preds)) / (sum(preds == 1) + 0.0000001)
    recall = float(sum(labels*preds)) / (sum(labels == 1) + 0.0000001)
    print 'precise', precise, 'recall', recall
    return 'score', 6*precise*recall / (5*recall+precise+0.0000001)


watchlist = [(dataset,'train'), (dataset_val,'val')]
bst = xgb.train(params,dataset,num_boost_round=2000,evals=watchlist, feval=evalerror)
#bst.save_model(model_dir+'model.model')
bst.save_model('train.model')