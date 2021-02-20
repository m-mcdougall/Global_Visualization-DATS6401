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

#The education dataset from Worldbank is missing many values in the timeframe we're looking at
#We'll load a supplimental dataset from OECD, and fill in the missing values
# The OECD Dataset itself is too small to be used on its own.


def process_education(df_in):
    
    
    df_in=df_in.drop(['INDICATOR', 'SUBJECT', 'MEASURE', 'FREQUENCY', 'Flag Codes'], axis=1)
    df_in['TIME']=df_in['TIME'].astype(str)
    df_in=df_in.pivot(index='LOCATION', columns='TIME', values='Value')
    df_in.index.name='Country Code'
    
    return df_in
        

#Load and process the supplimental dataframe
supplimental=pd.read_csv(os.path.abspath(wd+'//Data//DP_LIVE_19022021234709194.csv'))
supplimental=process_education(supplimental)


#Load the main education dataframe
edu=os.path.abspath(wd+'//Data//API_SE.XPD.TOTL.GD.ZS_DS2_en_csv_v2_1926663.csv', )
edu=pd.read_csv(edu, skiprows=[0,1,2])

#Set education index to countrycode, for merging
edu=edu.set_index('Country Code')

#Get the intersection of the two daaframes for filling
edu_fill=edu.index.intersection(supplimental.index)
edu_fill=edu.loc[edu_fill,:]

#If value is na in the main dataframe, get the missing value from the matching index in the supplimental
edu_fill=edu_fill.fillna(supplimental)

#Merge the filled in dataframe back into the original
edu=edu_fill.combine_first(edu)

#Reformat to match the other dataframes
edu=edu.reset_index()
edu=edu.set_index('Country Name')


del supplimental, edu_fill


#%%

#Import the rest of the data
#Will need additional pre-processing
#Education is currently expressed as a percentage of GDP, will need to be converted.


mil=os.path.abspath(wd+'//Data//API_MS.MIL.XPND.CD_DS2_en_csv_v2_1928211.csv')
mil=pd.read_csv(mil, skiprows=[0,1,2], index_col='Country Name')


gdp=os.path.abspath(wd+'//Data//API_MS.MIL.XPND.CD_DS2_en_csv_v2_1928211.csv')
gdp=pd.read_csv(gdp, skiprows=[0,1,2], index_col='Country Name')


pop=os.path.abspath(wd+'//Data//API_SP.POP.TOTL_DS2_en_csv_v2_1976634.csv')
pop=pd.read_csv(pop, skiprows=[0,1,2], index_col='Country Name')



#Education is currently expressed as a % of gdp
#Convert it to Current USD for uniformity

for col in range(1960, 2020):
    edu[str(col)] = gdp[str(col)]*edu[str(col)]/100


#Now all financial measures are in USD.
del col
#%%
#Collect data
data={'MIL':mil, 'GDP':gdp, 'EDU':edu, 'POP':pop}

for key in data:
    data[key]=data[key].drop(['Country Code', 'Indicator Name', 'Indicator Code', '2020', 'Unnamed: 65'], axis=1)


#%%
    
def plot_percent_non_null(df_in):
    """
    Plots the percentage of data present in the dataset
    
    df_in: The Dataframe of years of data
    """
    
    x=((df_in.shape[0]-(df_in.isnull().sum()))/df_in.shape[0])*100
    
    fig, ax = plt.subplots(figsize=[9,3])
    ax.plot(range(int(df_in.columns[0]),int(df_in.columns[-1])+1), x)
    plt.ylabel('% Non-null Datapoints')
    plt.xlabel('Year')
    plt.title(f'% Data Present - {key}')

    plt.show()

for key in data:
        plot_percent_non_null(data[key])
    
#%%

for key in data:
    data[key]=data[key].filter([str(i) for i in range(2010,2016)], axis=1)
    plot_percent_non_null(data[key])
#%%



def drop_non_reporters(df_in, max_percent_missing=0.6):
    """
    Drops countries from dataset if they have more than a given percent 
    of their data missing
    
    df_in: The Dataframe of years of data
    max_percent_missing: The maximum percent of missing data that is acceptable
    """
    
    #Find number of missing datapoints for each country
    years=df_in.shape[1]
    missing_count=df_in.isna().sum(axis=1)
    
    #Filter out countries whose missing datapoints exceed the maximum
    keep=missing_count<years*max_percent_missing
    
    print(f'\n---------------------')
    print(f'\n The Following Countries have been Removed:\n\n{df_in[~keep].index.values}')
    print(f'\n---------------------')
    return df_in[keep]

   


for key in data:
    data[key]=drop_non_reporters(data[key], max_percent_missing=0.8)
    plot_percent_non_null(data[key])




#%%
    
    

























    