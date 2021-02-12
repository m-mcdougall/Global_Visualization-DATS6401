# -*- coding: utf-8 -*-


import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import numpy as np
import seaborn as sns


#Set working directory
wd=os.path.abspath('C://Users//Mariko//Documents//GitHub//Global_Visualization-DATS6401//')
os.chdir(wd)


#%%

#Import all data
#Will need additional pre-processing
#Education is currently expressed as a percentage of GDP, will need to be converted.


mil=os.path.abspath(wd+'//Data//API_MS.MIL.XPND.CD_DS2_en_csv_v2_1928211.csv')
mil=pd.read_csv(mil, skiprows=[0,1,2], index_col='Country Name')


gdp=os.path.abspath(wd+'//Data//API_MS.MIL.XPND.CD_DS2_en_csv_v2_1928211.csv')
gdp=pd.read_csv(gdp, skiprows=[0,1,2], index_col='Country Name')



edu=os.path.abspath(wd+'//Data//API_SE.XPD.TOTL.GD.ZS_DS2_en_csv_v2_1926663.csv')
edu=pd.read_csv(edu, skiprows=[0,1,2], index_col='Country Name')



pop=os.path.abspath(wd+'//Data//API_SP.POP.TOTL_DS2_en_csv_v2_1976634.csv')
pop=pd.read_csv(pop, skiprows=[0,1,2], index_col='Country Name')


#Collect data
data={'MIL':mil, 'GDP':gdp, 'EDU':edu, 'POP':pop}

for key in data:
    data[key]=data[key].drop(['Country Code', 'Indicator Name', 'Indicator Code', '2020', 'Unnamed: 65'], axis=1)

df_in=data['MIL']

x=(df_in.shape[0]-(df_in.isnull().sum()))

fig, ax = plt.subplots(figsize=[9,3])
ax.plot(range(1960,2020), x)
#ax.plot(x)

#plt.xticks(rotation=45)
#ax.set_xticklabels(ax.get_xticklabels(),rotation=45, horizontalalignment='right')
plt.ylabel('# Non-null Datapoints')
plt.xlabel('Year')
