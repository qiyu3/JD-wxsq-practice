# -*- coding: utf-8 -*-

import os.path as osp
import pandas as pd
import numpy as np
import datetime




# 提取文件目录
dir_root = osp.dirname(__file__)
data_dir = osp.abspath(osp.join(dir_root,  'data'))

behavioral = pd.read_csv(data_dir+'/behavioral_tm.csv')
best_item = pd.read_csv(data_dir+'/best_item.csv')

#将不存在于best_item中的三级品类数据从behavioral中删去
item = best_item.item_third_cate_cd.drop_duplicates()
item = pd.DataFrame(item)
behavioral = pd.merge(behavioral,item)

behavioral = behavioral.dropna()
best_item = best_item.dropna()




#筛选出行为数据中类型为点击的数据
def get_click_data(data):
	data_click = data[data.act_type==1]
	return data_click

#对第三品类出现次数进行统计
def get_third_cate_counts(data):
	third_cate_counts = data.item_third_cate_cd.value_counts()
	third_cate_counts.to_csv(data_dir+'/keshan_best_item_counts.csv')

#从item中筛选出第三品类排名靠前的商品，best_item为排名靠前的第三品类集合
def get_best_third_cate_item(item,best_item):
	item.item_third_cate_cd = item.item_third_cate_cd.astype('int')
	best_item.item_third_cate_cd = best_item.item_third_cate_cd.astype('int')
	item_in_best = pd.merge(item,best_item,on=['item_third_cate_cd'])
	item_in_best.to_csv(data_dir+'/best_item.csv',index = False)

#将形如‘2016-01-01’的字符串转为标准的datetime的格式
def str_to_date(date):
        return datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])) 

# 日期递增   
def add(date, delta):
    date = str_to_date(date)
    new_date = date + datetime.timedelta(delta)
    return new_date.strftime('%Y-%m-%d')

# 两个日期相减
def subtract(date1, date2):
    return (str_to_date(date1) - str_to_date(date2)).days

# 从item表中算出某一品类对应的商品数量
def get_skunum_of_cate(item,cate_type,cate):
	if cate_type==1 :
		item = item[item.item_first_cate_cd==cate]
	elif cate_type==2 :
		item = item[item.item_second_cate_cd==cate]
	elif cate_type==3 :
		item = item[item.item_third_cate_cd==cate]
	return item.shape[0]

# 从行为数据表中获取某品类的某种操作次数
def get_actionnum_of_cate(behavioral,cate_type,cate,action_type):
	behavioral = behavioral[behavioral.act_type==action_type]
	if cate_type==1 :
		behavioral = behavioral[behavioral.item_first_cate_cd==cate]
	elif cate_type==2 :
		behavioral = behavioral[behavioral.item_second_cate_cd==cate]
	elif cate_type==3 :
		behavioral = behavioral[behavioral.item_third_cate_cd==cate]
	return behavioral.shape[0]


'''
#改变时间格式
behavioral.tm = behavioral.tm.apply(str_to_date)
behavioral.to_csv('C:/Users/acer/Desktop/JD-wxsq-practice/data/behavioral_tm.csv',index = False)

'''




date = '2017-07-05'
while date <= '2017-08-16':  #'2017-08-16'
	enddate = add(date,6)
	time_data = behavioral[behavioral.tm >= date]
	time_data = time_data[time_data.tm <= enddate]
	openid = time_data['openid'].unique()
	user_third = pd.DataFrame(columns=['openid','item_third_cate_cd'])
	for op_id in openid :
		id_data = time_data[time_data.openid == op_id]
		third_cate = id_data['item_third_cate_cd'].unique()
		for cate in third_cate :
			new_user_third = pd.DataFrame({'openid':[op_id],'item_third_cate_cd':[cate]})
			user_third = user_third.append(new_user_third,ignore_index = True)
	
	


	feature_all = pd.DataFrame()
	#对每一个user—cate提取特征
	for i in range(0,user_third.shape[0]):
		o_id = user_third.loc[i].openid
		third = user_third.loc[i].item_third_cate_cd

		the_user_data = time_data[time_data.openid == o_id]
		user_age = the_user_data.iloc[0].age
		user_sex = the_user_data.iloc[0].sex

		the_cate_data = time_data[time_data.item_third_cate_cd == third]
		first = the_cate_data.iloc[0].item_first_cate_cd
		second = the_cate_data.iloc[0].item_second_cate_cd




		#该一二三级品类商品数量
		cate_first_num = get_skunum_of_cate(best_item,1,first)
		cate_second_num = get_skunum_of_cate(best_item,2,second)
		cate_third_num = get_skunum_of_cate(best_item,3,third)

		#该一二三级品类各种操作次数
		cate_first_act0 = get_actionnum_of_cate(time_data,1,first,0)
		cate_first_act1 = get_actionnum_of_cate(time_data,1,first,1)
		cate_first_act2 = get_actionnum_of_cate(time_data,1,first,2)
		cate_first_act3 = get_actionnum_of_cate(time_data,1,first,3)
		cate_first_act_all = cate_first_act0 + cate_first_act1 +cate_first_act2 +cate_first_act3

		cate_second_act0 = get_actionnum_of_cate(time_data,2,second,0)
		cate_second_act1 = get_actionnum_of_cate(time_data,2,second,1)
		cate_second_act2 = get_actionnum_of_cate(time_data,2,second,2)
		cate_second_act3 = get_actionnum_of_cate(time_data,2,second,3)
		cate_second_act_all = cate_second_act0 + cate_second_act1 +cate_second_act2 +cate_second_act3

		cate_third_act0 = get_actionnum_of_cate(time_data,3,third,0)
		cate_third_act1 = get_actionnum_of_cate(time_data,3,third,1)
		cate_third_act2 = get_actionnum_of_cate(time_data,3,third,2)
		cate_third_act3 = get_actionnum_of_cate(time_data,3,third,3)
		cate_third_act_all = cate_third_act0 + cate_third_act1 +cate_third_act2 +cate_third_act3

		#该用户对该品类的行为特征
		#时间段内最早与最晚操作
		the_date = date
		day = time_data[time_data.tm == the_date]
		day = day[day.openid == o_id]
		day = day[day.item_third_cate_cd == third]
		if day.shape[0] == 0:
			day1 = 0
		else :
			day1 = 1

		the_date = add(the_date,1)
		day = time_data[time_data.tm == the_date]
		day = day[day.openid == o_id]
		day = day[day.item_third_cate_cd == third]
		if day.shape[0] == 0:
			day2 = 0
		else :
			day2 = 1

		the_date = add(the_date,1)
		day = time_data[time_data.tm == the_date]
		day = day[day.openid == o_id]
		day = day[day.item_third_cate_cd == third]
		if day.shape[0] == 0:
			day3 = 0
		else :
			day3 = 1

		the_date = add(the_date,1)
		day = time_data[time_data.tm == the_date]
		day = day[day.openid == o_id]
		day = day[day.item_third_cate_cd == third]
		if day.shape[0] == 0:
			day4 = 0
		else :
			day4 = 1

		the_date = add(the_date,1)
		day = time_data[time_data.tm == the_date]
		day = day[day.openid == o_id]
		day = day[day.item_third_cate_cd == third]
		if day.shape[0] == 0:
			day5 = 0
		else :
			day5 = 1

		the_date = add(the_date,1)
		day = time_data[time_data.tm == the_date]
		day = day[day.openid == o_id]
		day = day[day.item_third_cate_cd == third]
		if day.shape[0] == 0:
			day6 = 0
		else :
			day6 = 1

		the_date = add(the_date,1)
		day = time_data[time_data.tm == the_date]
		day = day[day.openid == o_id]
		day = day[day.item_third_cate_cd == third]
		if day.shape[0] == 0:
			day7 = 0
		else :
			day7 = 1


		#该用户该一二三级品类各种操作次数
		

		user_cate_first_act0 = get_actionnum_of_cate(the_user_data,1,first,0)
		user_cate_first_act1 = get_actionnum_of_cate(the_user_data,1,first,1)
		user_cate_first_act2 = get_actionnum_of_cate(the_user_data,1,first,2)
		user_cate_first_act3 = get_actionnum_of_cate(the_user_data,1,first,3)
		user_cate_first_act_all = cate_first_act0 + cate_first_act1 +cate_first_act2 +cate_first_act3

		user_cate_second_act0 = get_actionnum_of_cate(the_user_data,2,second,0)
		user_cate_second_act1 = get_actionnum_of_cate(the_user_data,2,second,1)
		user_cate_second_act2 = get_actionnum_of_cate(the_user_data,2,second,2)
		user_cate_second_act3 = get_actionnum_of_cate(the_user_data,2,second,3)
		user_cate_second_act_all = cate_second_act0 + cate_second_act1 +cate_second_act2 +cate_second_act3

		user_cate_third_act0 = get_actionnum_of_cate(the_user_data,3,third,0)
		user_cate_third_act1 = get_actionnum_of_cate(the_user_data,3,third,1)
		user_cate_third_act2 = get_actionnum_of_cate(the_user_data,3,third,2)
		user_cate_third_act3 = get_actionnum_of_cate(the_user_data,3,third,3)
		user_cate_third_act_all = cate_third_act0 + cate_third_act1 +cate_third_act2 +cate_third_act3

		#获得标签
		begindate = add(date,7)
		enddate = add(begindate,6)
		new_time_data = behavioral[behavioral.tm >= begindate]
		new_time_data = new_time_data[new_time_data.tm <= enddate]
		label_data = new_time_data[new_time_data.act_type == 1]
		label_data = label_data[label_data.openid == o_id]
		label_data = label_data[label_data.item_third_cate_cd == third]
		if label_data.shape[0] == 0 :
			label_value = 0
		else :
			label_value = 1


		feature_user = pd.DataFrame({'sex':[user_sex],'age':[user_age]})
		feature_act_time = pd.DataFrame({'day1':[day1],'day2':[day2],'day3':[day3],'day4':[day4],'day5':[day5],'day6':[day6],'day7':[day7]})

		feature_cate_num = pd.DataFrame({'cate_first_num':[cate_first_num],'cate_second_num':[cate_second_num],'cate_third_num':[cate_third_num]})
		feature_cate_first_act = pd.DataFrame({'cate_first_act0':[cate_first_act0],'cate_first_act1':[cate_first_act1],'cate_first_act2':[cate_first_act2],'cate_first_act3':[cate_first_act3],'cate_first_act_all':[cate_first_act_all]})
		feature_cate_second_act = pd.DataFrame({'cate_second_act0':[cate_second_act0],'cate_second_act1':[cate_second_act1],'cate_second_act2':[cate_second_act2],'cate_second_act3':[cate_second_act3],'cate_second_act_all':[cate_second_act_all]})
		feature_cate_third_act = pd.DataFrame({'cate_third_act0':[cate_third_act0],'cate_third_act1':[cate_third_act1],'cate_third_act2':[cate_third_act2],'cate_third_act3':[cate_third_act3],'cate_third_act_all':[cate_third_act_all]})

		feature_user_cate_first_act = pd.DataFrame({'user_cate_first_act0':[user_cate_first_act0],'user_cate_first_act1':[user_cate_first_act1],'user_cate_first_act2':[user_cate_first_act2],'user_cate_first_act3':[user_cate_first_act3],'user_cate_first_act_all':[user_cate_first_act_all]})
		feature_user_cate_second_act = pd.DataFrame({'user_cate_second_act0':[user_cate_second_act0],'user_cate_second_act1':[user_cate_second_act1],'user_cate_second_act2':[user_cate_second_act2],'user_cate_second_act3':[user_cate_second_act3],'user_cate_second_act_all':[user_cate_second_act_all]})
		feature_user_cate_third_act = pd.DataFrame({'user_cate_third_act0':[user_cate_third_act0],'user_cate_third_act1':[user_cate_third_act1],'user_cate_third_act2':[user_cate_third_act2],'user_cate_third_act3':[user_cate_third_act3],'user_cate_third_act_all':[user_cate_third_act_all]})

		label = pd.DataFrame({'label':[label_value]})
		feature_user_third = pd.DataFrame({'openid':[o_id],'item_third_cate_cd':[third]})


		feature_one_data = pd.concat([feature_user_third,feature_user,feature_cate_num,feature_cate_first_act,feature_cate_second_act,feature_cate_third_act,feature_user_cate_first_act,feature_user_cate_second_act,feature_user_cate_third_act,feature_act_time,label],axis=1)
		feature_all = feature_all.append(feature_one_data,ignore_index = True)


	feature_all.to_csv(osp.abspath(dir_root)+'/feature_label'+date+'.csv',index = False)
	date = add(date,7)








#behavioral = behavioral[behavioral.tm<'2017-07-05']
#print behavioral.shape[0]

