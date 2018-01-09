# JD-wxsq-practice
将behavioral.csv放到data文件夹，运行time_format.py，得到标准时间格式的behavioral_tm.csv文件，然后直接运行run.sh即可。


代码文件及可调参数说明：

feature.py-----------------提取训练特征
读取behavioral.csv和item.csv，以一周为时间间隔提取特征
输出7份feature_label.csv特征数据，分别代表七周时间['2017-07-05','2017-07-12','2017-07-19','2017-07-26','2017-08-02','2017-08-09','2017-08-16']


feature_for_predict.py-----提取用于预测的特征
提取从'2017-08-25'开始的最后一周的特征，输出一份特征数据

train_model.py-------------训练模型
读取7份训练特征数据，其中6份用于训练，1份用于验证
可调节模型参数，训练轮数，评估函数
输出模型文件train.model

predict.py-----------------预测结果
读取模型文件train.model和预测特征数据进行预测得到预测结果
预测结果中仅保留item.csv中存在的三级品类，并过滤低于阈值的结果（item.csv可换成其他更小的商品子集）
输出文件为predict_result.csv
