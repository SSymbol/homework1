# coding: utf-8
import operator
from pandas import Series
import matplotlib
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
import numpy as np
import time
import pandas
import json
import math
import stats
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')


# **Step1. 读取数据**
# - 读取csv文件，生成data frame
# 定义两类数据：标称型和数值型
#数据集1

name_category = ['GameID', 'time', 'SideofField', 'FirstDown', 'posteam', 'DefensiveTeam', 'desc',
                 'PlayAttempted', 'Yards.Gained', 'sp', 'Touchdown', 'ExPointResult', 'TwoPointConv', 'DefTwoPoint',
                 'Onsidekick', 'Safety', 'PuntResult', 'PlayType', 'Passer', 'Passer_ID', 'PassAttempt',
                 'PassOutcome', 'PassLength', 'QBHit', 'PassLocation', 'InterceptionThrown', 'Interceptor', 'Rusher',
                 'Rusher_ID', 'RushAttempt', 'RunLocation', 'RunGap', 'Receiver', 'Receiver_ID', 'Reception',
                 'ReturnResult', 'Returner', 'BlockingPlayer', 'Tackler1', 'Tackler2', 'FieldGoalResult', 'Fumble',
                 'RecFumbTeam', 'RecFumbPlayer', 'Sack', 'Challenge.Replay', 'ChalReplayResult', 'Accepted.Penalty',
                 'PenalizedTeam', 'PenaltyType', 'PenalizedPlayer', 'HomeTeam', 'AwayTeam', 'Timeout_Indicator',
                 'Timeout_Team', 'Season', 'posteam_timeouts_pre', 'HomeTimeouts_Remaining_Pre',
                 'AwayTimeouts_Remaining_Pre', 'HomeTimeouts_Remaining_Post', 'AwayTimeouts_Remaining_Post']
name_value = ['Drive', 'qtr', 'down', 'TimeUnder', 'TimeSecs', 'PlayTimeDiff', 'yrdln', 'yrdline100', 'ydstogo',
              'ydsnet', 'GoalToGo', 'AirYards', 'YardsAfterCatch', 'FieldGoalDistance', 'Penalty.Yards',
              'PosTeamScore', 'DefTeamScore', 'ScoreDiff', 'AbsScoreDiff', 'No_Score_Prob', 'Opp_Field_Goal_Prob',
              'Opp_Safety_Prob', 'Opp_Touchdown_Prob', 'Field_Goal_Prob', 'Safety_Prob', 'Touchdown_Prob',
              'ExPoint_Prob', 'TwoPoint_Prob', 'ExpPts', 'EPA', 'airEPA', 'yacEPA', 'Home_WP_pre', 'Away_WP_pre',
              'Home_WP_post', 'Away_WP_post', 'Win_Prob', 'WPA', 'airWPA', 'yacWPA']
'''

#数据集2
name_category = ['Permit Number', 'Permit Type', 'Permit Type Definition', 'Permit Creation Date', 'Block', 'Lot',
                 'Street Number', 'Street Number Suffix', 'Street Name', 'Street Suffix', 'Unit Suffix',
                 'Description', 'Current Status', 'Current Status Date', 'Filed Date', 'Issued Date',
                 'Completed Date', 'First Construction Document Date', 'Structural Notification', 'Fire Only Permit',
                 'Permit Expiration Date', 'Existing Use', 'Proposed Use', 'Plansets', 'TIDF Compliance',
                 'Existing Construction Type', 'Existing Construction Type Description',
                 'Proposed Construction Type', 'Proposed Construction Type Description','Site Permit',
                 'Neighborhoods - Analysis Boundaries', 'Zipcode', 'Location'];
name_value = ['Unit', 'Number of Existing Stories', 'Number of Proposed Stories', 'Estimated Cost',
              'Revised Cost', 'Existing Units', 'Proposed Units', 'Supervisor District'];
'''


#DataFile = open("E:/Building_Permits.csv",encoding='gb18030',errors='ignore')

DataFile = open("E:/NFL Play by Play 2009-2017 (v4).csv",encoding='gb18030',errors='ignore')

DataTable = pandas.read_csv(DataFile,low_memory=False);
DataTable = DataTable.dropna(axis=1, how='all');

# **Step 2. 数据摘要**
# 
# - 对标称属性，给出每个可能取值的频数

# 使用value_counts函数统计每个标称属性的取值频数
for item in name_category:
    print (item, '的频数为：\n', pd.value_counts(DataTable[item].values), '\n')


# - 对数值属性，给出最大、最小、均值、中位数、四分位数及缺失值的个数。

# 最大值
data_show= pd.DataFrame(data = DataTable[name_value].max(), columns = ['max'])
# 最小值
data_show['min'] = DataTable[name_value].min()
# 均值
data_show['mean'] = DataTable[name_value].mean()
# 中位数
data_show['median'] = DataTable[name_value].median()
# 四分位数
#data_show['quartile'] = DataTable[name_value].describe().loc['quartile']
#data_show['quartile']=stats.quantile(DataTable[name_value],p=0.25)
# 缺失值个数
data_show['missing'] = DataTable[name_value].describe().loc['count'].apply(lambda x : 200-x)

print (data_show)


# **Step 3. 数据可视化 **
# 
# - 针对数值属性：
# 绘制直方图，如mxPH，用qq图检验其分布是否为正态分布。

# 直方图
fig = plt.figure(figsize = (20,15))
i = 1
for item in name_value:
    ax = fig.add_subplot(6, 7, i)
    DataTable[item].plot(kind = 'hist', title = item, ax = ax)
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
fig.savefig('./image/histogram.png')
print ('histogram saved at ./image/histogram.png')


# qq图
fig = plt.figure(figsize = (20,15))
i = 1
for item in name_value:ax = fig.add_subplot(6, 7, i)
sm.qqplot(DataTable[item], ax = ax)
ax.set_title(item)
i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
fig.savefig('./image/qqplot.png')
print ('qqplot saved at ./image/qqplot.png')

# 从qq图中可以看出，只有mxPH和mnO2两项值符合正态分布，其他值均不符合

# - 绘制盒图，对离群值进行识别。
# 盒图
fig = plt.figure(figsize = (20,15))
i = 1
for item in name_value:
    ax = fig.add_subplot(6, 7, i)
    DataTable[item].plot(kind = 'box')
    i += 1
fig.savefig('./image/boxplot.png')
print ('boxplot saved at ./image/boxplot.png')


# **Step 4. 数据缺失的处理**
# 找出含有缺失值的数据条目索引值
nan_list = pd.isnull(DataTable).any(1).nonzero()[0]
# 4.1 将缺失部分剔除
data_filtrated = DataTable
#DataTable=DataFile;
# 绘制可视化图
fig = plt.figure(figsize = (20,15))
i = 6
# 对数值属性，绘制直方图
for item in name_value:
    ax = fig.add_subplot(8, 9, i)
    #ax = fig.add_subplot(4, 5, i)
    data_filtrated[item]=data_filtrated[item].dropna()
    ax.set_title(item)
    DataTable[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'filtrated', legend = True)
    ax.axvline(DataTable[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'b')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

# 保存图像和处理后数据
fig.savefig('./image/missing_data_delete.png')
print ('filted_missing_data1 saved at ./image/missing_data_delete.png')

# 4.2 最高频率值来填补缺失值
# 建立原始数据的拷贝
data_filtrated = DataTable.copy()
# 对每一列数据，分别进行处理
for item in name_category+name_value:
    # 计算最高频率的值
    most_frequent_value = data_filtrated[item].value_counts().idxmax()
    # 替换缺失值
    data_filtrated[item].fillna(value = most_frequent_value, inplace = True)

# 绘制可视化图
fig = plt.figure(figsize = (20,15))

i = 1
# 对标称属性，绘制折线图
for item in name_category:
    ax = fig.add_subplot(8, 9, i)
    ax.set_title(item)
    pd.value_counts(DataTable[item].values).plot(ax = ax, marker = '^', label = 'origin', legend = True)
    pd.value_counts(data_filtrated[item].values).plot(ax = ax, marker = 'o', label = 'filtrated', legend = True)
    i += 1    

i = 6
# 对数值属性，绘制直方图
for item in name_value:
    ax = fig.add_subplot(8, 9, i)
    ax.set_title(item)
    DataTable[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'droped', legend = True)
    ax.axvline(DataTable[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'b')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

# 保存图像和处理后数据
fig.savefig('./image/missing_data_most.png')
print ('filted_missing_data2 saved at ./image/missing_data_most.png')

# 4.3 通过属性的相关关系来填补缺失值
# 建立原始数据的拷贝
data_filtrated = DataTable.copy()
# 对数值型属性的每一列，进行插值运算
for item in name_value:
    data_filtrated[item].interpolate(inplace = True)
fig = plt.figure(figsize = (20,15))
i = 1
# 对标称属性，绘制折线图
for item in name_category:
    ax = fig.add_subplot(8, 9, i)
    ax.set_title(item)
    pd.value_counts(DataTable[item].values).plot(ax = ax, marker = '^', label = 'origin', legend = True)
    pd.value_counts(data_filtrated[item].values).plot(ax = ax, marker = 'o', label = 'filtrated', legend = True)
    i += 1   
    
i = 6
# 对数值属性，绘制直方图
for item in name_value:
    ax = fig.add_subplot(8, 9, i)
    ax.set_title(item)
    DataTable[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'droped', legend = True)
    ax.axvline(DataTable[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'b')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

fig.savefig('./image/missing_data_corelation.png')
print ('filted_missing_data3 saved at ./image/missing_data_corelation.png')


'''
# 4.4 通过数据对象之间的相似性来填补缺失值
data_norm = DataTable.copy()
data_norm[name_value] = data_norm[name_value].fillna(0)
data_norm[name_value] = data_norm[name_value].apply(lambda x : (x - np.mean(x)) / (np.max(x) - np.min(x)))
# 构造分数表
score = {}
range_length = len(DataTable)
for i in range(0, range_length):
    score[i] = {}
    for j in range(0, range_length):
        score[i][j] = 0    

for i in range(0, range_length):
    for j in range(i, range_length):
        for item in name_category:
            if data_norm.iloc[i][item] != data_norm.iloc[j][item]:
                score[i][j] += 1
        for item in name_value:
            temp = abs(data_norm.iloc[i][item] - data_norm.iloc[j][item])
            score[i][j] += temp
        score[j][i] = score[i][j]

data_filtrated = DataTable.copy()
for index in nan_list:
    best_friend = sorted(score[index].items(), key=operator.itemgetter(1), reverse = False)[1][0]
    for item in name_value:
        if pd.isnull(data_filtrated.iloc[index][item]):
            if pd.isnull(DataTable.iloc[best_friend][item]):
                data_filtrated.ix[index, item] = DataTable[item].value_counts().idxmax()
            else:
                data_filtrated.ix[index, item] = DataTable.iloc[best_friend][item]
fig = plt.figure(figsize = (20,15))
i = 1
# 对标称属性，绘制折线图
for item in name_category:
    ax = fig.add_subplot(4, 5, i)
    ax.set_title(item)
    pd.value_counts(DataTable[item].values).plot(ax = ax, marker = '^', label = 'origin', legend = True)
    pd.value_counts(data_filtrated[item].values).plot(ax = ax, marker = 'o', label = 'filtrated', legend = True)
    i += 1   
    
i = 6
# 对数值属性，绘制直方图
for item in name_value:
    ax = fig.add_subplot(4, 5, i)
    ax.set_title(item)
    DataTable[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'droped', legend = True)
    ax.axvline(DataTable[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'b')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

# 保存图像和处理后数据
fig.savefig('./image/missing_data_similarity.png')
print ('filted_missing_data4 saved at ./image/filted_missing_data4.png')
'''
