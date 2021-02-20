# -*- coding: utf-8 -*-


import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression


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




#Import the rest of the data
#Will need additional pre-processing
#Education is currently expressed as a percentage of GDP, will need to be converted.


mil=os.path.abspath(wd+'//Data//API_MS.MIL.XPND.CD_DS2_en_csv_v2_1928211.csv')
mil=pd.read_csv(mil, skiprows=[0,1,2], index_col='Country Name')


gdp=os.path.abspath(wd+'//Data//API_NY.GDP.MKTP.CD_DS2_en_csv_v2_2001204.csv')
gdp=pd.read_csv(gdp, skiprows=[0,1,2], index_col='Country Name')


pop=os.path.abspath(wd+'//Data//API_SP.POP.TOTL_DS2_en_csv_v2_1976634.csv')
pop=pd.read_csv(pop, skiprows=[0,1,2], index_col='Country Name')


health=os.path.abspath(wd+'//Data//API_SH.XPD.CHEX.GD.ZS_DS2_en_csv_v2_2055594.csv')
health=pd.read_csv(health, skiprows=[0,1,2], index_col='Country Name')

#Education and healthcare are currently expressed as a % of gdp
#Convert them to Current USD for uniformity

for col in range(1960, 2020):
    edu[str(col)] = gdp[str(col)]*edu[str(col)]/100

for col in range(1960, 2020):
    health[str(col)] = gdp[str(col)]*health[str(col)]/100



#Now all financial measures are in USD.
del col
#%%
#Collect data
data={'MIL':mil, 'GDP':gdp, 'EDU':edu, 'POP':pop, 'HEAL':health}

for key in data:
    data[key]=data[key].drop(['Country Code', 'Indicator Name', 'Indicator Code', '2020', 'Unnamed: 65'], axis=1)

del [mil, gdp,edu,pop,health]
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
    data[key]=data[key].filter([str(i) for i in range(2011,2018)], axis=1)
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

   

#Remove Countries that are missing >80% of their data 
#for key in data:
#    data[key]=drop_non_reporters(data[key], max_percent_missing=0.8)
#    plot_percent_non_null(data[key])


#%%
    
def linear_reg_fill_data(data_in):
    """
    Takes a dataframe of countries with missing data and runs a linear regression to predict and infill the values of 
    the missing datas. 
    Each country requires at least 2 datapoints present to run the regression.
    Countries with less than the minimum number of datapoints are converted fully into nans
    
    Returns the complete dataframe with original data and filled in predicted values.
    
    df_in: The Dataframe of years of data
    """
    
    
    
    def linear_reg_fill(country_in):
        """
        Takes a country series with missing data and runs a linear regression to predict the values of 
        the nans. Requires at least 2 datapoints to run the regression.
        Returns the series with original data and filled in predicted values.
        
        country_in: A country series that is missing at least 1 datapoint, and has at least 2 existing datapoints.
        """
        
        #Seperate out the null and non-null components
        not_null = country_in[country_in.notnull()]
        yes_null = country_in[~country_in.notnull()]
            
        #Fit the regression on available data
        reg = LinearRegression().fit(not_null.index.values.astype(int).reshape(-1, 1), not_null.values.reshape(-1, 1))
        
        #predict the missing values and in-fill the missing data
        pred = reg.predict(yes_null.index.values.astype(int).reshape(-1, 1))
        yes_null.loc[:]=pred.reshape(-1, )
        
        #Merge into one series and return
        country_in=pd.concat([not_null, yes_null])
        
        return country_in
    
    
    
    
    #Collection list to be converted to df later
    filled_data=[]
    
    for i in range(data_in.shape[0]):
        
        #Run for one country at a time 
        this_country = data_in.iloc[i,:].copy()
        
        # If the country has minimum 2 datapoints, run a linear model on the data to fill in any nan values
        # If if doesn't turn all values to nan
        
        #If all datapoints are present
        if this_country.notnull().sum()==this_country.shape[0]:
            pass
        
        #If there is one or 0 datapoint we cannot use the data.
        elif this_country.notnull().sum() <=1:
            this_country.loc[:] = np.nan
        
        #There is missing data, but enought to fit the model
        else:
            this_country=linear_reg_fill(this_country)
            
        #Append to the collector
        filled_data.append(this_country)    
    
    #Concat into one dataframe    
    filled_data=pd.DataFrame(filled_data)
    
    return filled_data




#%%

for key in data:
    data[key]=linear_reg_fill_data(data[key])
    plot_percent_non_null(data[key]) 


#%%
"""
Need to remove some of the rows that represent economies rather than countries

Skim the top 40 of each set and drop all non-country entries found.

"""    
    
not_a_country=np.array([])
    
 #Check if a   

for key in data:
    #print(data[key].sort_values('2017', ascending=False).head(40))
    not_a_country=np.append(not_a_country,data[key].sort_values('2017', ascending=False).head(40).index.values)


not_a_country=list(set(not_a_country))

not_a_country=[i for i in not_a_country if i not in ['Japan','Russian Federation','Saudi Arabia','Italy','Korea, Rep.' ,'Brazil',
                      'Germany', 'India', 'China', 'Israel', 'France', 'United States',
                      'United Kingdom', 'Australia', ]]

#Ran again, these are the last economies present
still_not_countries=['Other small states','Central Europe and the Baltics', 'Small states', ]

#Drop all the economies that are present
for key in data:
    data[key]=data[key].drop(not_a_country, axis=0)
    data[key]=data[key].drop(still_not_countries, axis=0)
   
del [not_a_country,still_not_countries]    
#%%
for key in data:
    print(f'\n\n ---------------  {key}  ---------------------\n\n')
    print(data[key].sort_values('2017', ascending=False).head(40))    
    

#%%
    
"""
Make the divided factors values
"""

#Extract the data from the dict

gdp=data['GDP']
pop=data['POP']


def per_capita(df_in, pop_in=pop):
    '''
    Returns The given stats as a per capita value
    
    df_in: The Dataframe of years of data
    pop_in: The Population Dataframe - default pop
    '''
    return df_in/pop_in

def per_GDP(df_in, gdp_in=gdp):
    '''
    Returns The given stats as a percent gdp value
    
    df_in: The Dataframe of years of data
    gdp_in: The GDP Dataframe - default pop
    '''
    return df_in/gdp_in*100



def rate_of_change(df_in):
    '''
    Calculates the absolute and percent change for each year
    Returns tuple of absolute change, percent change
    
    df_in: The Dataframe of years of data
    '''

    #Absolute Rate of change
    abs_delta=df_in.diff(axis=1)
    
    #Percent Rate of Change
    per_delta=df_in.pct_change(axis=1)
    
    return abs_delta, per_delta



#Per Capita
per_cap ={}
for key in data:
    per_cap[key]= per_capita(data[key])


#Percent_GDP
per_gdp ={}
for key in data:
    per_gdp[key]= per_GDP(data[key])


#Rate of Change    
abs_change ={}
per_change ={}
for key in data:
    abs_change[key],per_change[key] = rate_of_change(data[key])



del gdp, pop


#%%

def writer_helper(df_in, sheet_name_in, writer_engine):
    """
    Sorts and selects the top 10 countries for the dataframe inserted
    Selects the top 10 based of the final year's values.
    
    Returns the shortened daaframe
    """

    #Sort by final values and shorten
    df_out=df_in.sort_values(data[key].columns[-1], ascending=False)
    df_out=df_out.head(10)
    
    #Add the sheet
    df_out.to_excel(writer_engine, sheet_name=sheet_name_in) 




writer = pd.ExcelWriter('Processed_Data.xlsx', engine='xlsxwriter')

#The total numbers
for key in data:
    writer_helper(data[key], sheet_name_in='Values_'+key , writer_engine=writer)



    
#The per Capita numbers
for key in ['MIL', 'GDP', 'EDU', 'HEAL']:
    writer_helper(per_cap[key], sheet_name_in='Per_Capita_'+key , writer_engine=writer)


#The per GDP numbers
for key in ['MIL', 'EDU', 'HEAL']:
    writer_helper(per_gdp[key], sheet_name_in='Percent_GDP_'+key , writer_engine=writer)


#The absolute change numbers
for key in ['MIL', 'EDU', 'HEAL']:
    writer_helper(abs_change[key], sheet_name_in='Delta_ABS_'+key , writer_engine=writer)


#The percent change numbers
for key in ['MIL', 'EDU', 'HEAL']:
    writer_helper(per_change[key], sheet_name_in='Delta_PER_'+key , writer_engine=writer)


#Save and close the whole file
writer.save()




































    
    