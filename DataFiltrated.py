# coding = utf-8
import pandas
from pandas import Series
import matplotlib
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
import numpy as np
import time
import json
import math
import scipy.stats as stats
#DataFile = open("F:/Users/andy/Documents/HW/Building_Permits.csv",encoding='gb18030',errors='ignore')
DataFile = open("F:/Users/andy/Documents/HW/NFL Play by Play 2009-2017 (v4).csv",encoding='gb18030',errors='ignore')
DataTable = pandas.read_csv(DataFile);
DataTable = DataTable.dropna(axis=1, how='all');
# 标称属性
'''
NominalAttribute = ['Permit Number', 'Permit Type', 'Permit Type Definition', 'Permit Creation Date', 'Block', 'Lot',
                    'Street Number', 'Street Number Suffix', 'Street Name', 'Street Name Suffix', 'Unit suffix',
                    'Description', 'Current Status', 'Current Status Date', 'Filed Date', 'Issued Date',
                    'Completed Date', 'First Construction Document Date', 'Structural Notification', 'Fire Only Permit',
                    'Permit Expiration Date', 'Existing Use', 'Proposed Use', 'Plansets', 'TIDF Compliance',
                    'Existing Construction Type', 'Existing Construction Type Description',
                    'Proposed Construction Type', 'Proposed Construction Type DescriptionSite Permit',
                    'Neighborhoods - Analysis Boundaries', 'Zipcode', 'Location'];


# 数值属性
NumericAttribute = ['Unit', 'Number of Existing Stories', 'Number of Proposed Stories', 'Estimated Cost',
                    'Revised Cost', 'Existing Units', 'Proposed Units', 'Supervisor District'];
'''
NominalAttribute = ['Date', 'GameID', 'time', 'SideofField', 'FirstDown', 'posteam', 'DefensiveTeam', 'desc',
                    'PlayAttempted', 'Yards.Gained', 'sp', 'Touchdown', 'ExPointResult', 'TwoPointConv', 'DefTwoPoint',
                    'Onsidekick', 'Safety', 'PuntResult', 'PlayType', 'Passer', 'Passer_ID', 'PassAttempt',
                    'PassOutcome', 'PassLength', 'QBHit', 'PassLocation', 'InterceptionThrown', 'Interceptor', 'Rusher',
                    'Rusher_ID', 'RushAttempt', 'RunLocation', 'RunGap', 'Receiver', 'Receiver_ID', 'Reception',
                    'ReturnResult', 'Returner', 'BlockingPlayer', 'Tackler1', 'Tackler2', 'FieldGoalResult', 'Fumble',
                    'RecFumbTeam', 'RecFumbPlayer', 'Sack', 'Challenge.Replay', 'ChalReplayResult', 'Accepted.Penalty',
                    'PenalizedTeam', 'PenaltyType', 'PenalizedPlayer', 'HomeTeam', 'AwayTeam', 'Timeout_Indicator',
                    'Timeout_Team', 'Season', 'posteam_timeouts_pre', 'HomeTimeouts_Remaining_Pre',
                    'AwayTimeouts_Remaining_Pre', 'HomeTimeouts_Remaining_Post', 'AwayTimeouts_Remaining_Post'];
NumericAttribute = ['Drive', 'qtr', 'down', 'TimeUnder', 'TimeSecs', 'PlayTimeDiff', 'yrdln', 'yrdline100', 'ydstogo',
                    'ydsnet', 'GoalToGo', 'AirYards', 'YardsAfterCatch', 'FieldGoalDistance', 'Penalty.Yards',
                    'PosTeamScore', 'DefTeamScore', 'ScoreDiff', 'AbsScoreDiff', 'No_Score_Prob', 'Opp_Field_Goal_Prob',
                    'Opp_Safety_Prob', 'Opp_Touchdown_Prob', 'Field_Goal_Prob', 'Safety_Prob', 'Touchdown_Prob',
                    'ExPoint_Prob', 'TwoPoint_Prob', 'ExpPts', 'EPA', 'airEPA', 'yacEPA', 'Home_WP_pre', 'Away_WP_pre',
                    'Home_WP_post', 'Away_WP_post', 'Win_Prob', 'WPA', 'airWPA', 'yacWPA'];
BinaryAttribute = ['GoalToGo', 'FirstDown', 'sp', 'Touchdown', 'ExPointResult', 'Onsidekick', 'PuntResult',
                   'PassAttempt', 'PassOutcome', 'PassLength', 'QBHit', 'InterceptionThrown', 'RushAttempt'];
#'''
NumericAttributeAbstract = dict();
NominalAttributeAbstract = dict();
nan_list = pandas.isnull(DataTable).any(1).nonzero()[0]
DataTable_filtrated=DataTable;
#1删除
# 绘制可视化图
fig = pyplot.figure(figsize = (20,15))
n = 1
# 对数值属性，绘制直方图
for i in NumericAttribute:
    ax = fig.add_subplot(6, 7, n)
    
    DataTable_filtrated[i] = DataTable_filtrated[i].dropna()#删除
    ax.set_title(i)
    DataTable[i].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    DataTable_filtrated[i].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'filtrated', legend = True)
    #pyplot.show()
    ax.axvline(DataTable[i].mean(), color = 'r')
    ax.axvline(DataTable_filtrated[i].mean(), color = 'b')
    n += 1
pyplot.subplots_adjust(wspace = 0.3, hspace = 0.3)
# 保存图像和处理后数据
fig.savefig('missing_data_delete.png')
print ('filted_missing_data1 saved at missing_data_delete.png')
#2众数
# 绘制可视化图
DataTable_filtrated=DataTable;
fig = pyplot.figure(figsize = (20,15))
n = 1
# 对数值属性，绘制直方图
for i in NumericAttribute:
    ax = fig.add_subplot(6, 7, n)
    MostFrequentElement = DataTable[i].value_counts().idxmax();
                            
    DataTable_filtrated[i] = DataTable_filtrated[i].fillna(value=MostFrequentElement);  # 众数填补缺失值
    ax.set_title(i)
    DataTable[i].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    DataTable_filtrated[i].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'filtrated', legend = True)
    #pyplot.show()
    ax.axvline(DataTable[i].mean(), color = 'r')
    ax.axvline(DataTable_filtrated[i].mean(), color = 'b')
    n += 1
pyplot.subplots_adjust(wspace = 0.3, hspace = 0.3)
# 保存图像和处理后数据
fig.savefig('missing_data_most.png')
print ('filted_missing_data1 saved at missing_data_most.png')

#3属性相关 插值
# 绘制可视化图
fig = pyplot.figure(figsize = (20,15))
DataTable_filtrated=DataTable;

n = 1
# 对数值属性，绘制直方图
for i in NumericAttribute:
    ax = fig.add_subplot(6, 7, n)
                             
    DataTable_filtrated[i].interpolate(inplace = True)#插值
    ax.set_title(i)
    DataTable[i].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    DataTable_filtrated[i].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'filtrated', legend = True)
    #pyplot.show()
    ax.axvline(DataTable[i].mean(), color = 'r')
    ax.axvline(DataTable_filtrated[i].mean(), color = 'b')
    n += 1
pyplot.subplots_adjust(wspace = 0.3, hspace = 0.3)
# 保存图像和处理后数据
fig.savefig('missing_data_corelation.png')
print ('filted_missing_data1 saved at missing_data_corelation.png')

