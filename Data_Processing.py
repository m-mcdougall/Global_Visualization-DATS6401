# -*- coding: utf-8 -*-


import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
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
                      'United Kingdom', 'Australia','Canada' ]]

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


#Rename some country names from the WorldBank format to their more common names
for key in data:
    data[key].rename(index={'Russian Federation':'Russia','Iran, Islamic Rep.':'Iran', 'Korea, Rep.': 'South Korea',
        'Venezuela, RB':'Venezuela', 'Egypt, Arab Rep.':'Egypt', 'United Arab Emirates': 'UAE'}, inplace=True)

    

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


#Trend Rate of Change
trend_abs_change ={}
trend_per_change ={}

for key in data:
    trend_abs_change[key], trend_per_change[key] = rate_of_change(pd.concat([data[key].iloc[:,0] ,data[key].iloc[:,-1]], axis=1))


del gdp, pop





#%%
def writer_helper(df_in, parent_df, sheet_name_in, writer_engine):
    """
    Sorts and selects the top 10 countries for the dataframe inserted
    Selects the top 10 based of the final year's values.
    
    Returns the shortened daaframe
    """

    #Filter by the parent_df's final countries
    parent_filter = parent_df.sort_values(parent_df.columns[-1], ascending=False)
    parent_filter=parent_filter.head(10)
    df_out=df_in[df_in.index.isin(parent_filter.index)]
    #df_out = df_out.sort_values(df_out.columns[-1], ascending=False)

    
    #Add the sheet
    df_out.to_excel(writer_engine, sheet_name=sheet_name_in) 




writer = pd.ExcelWriter('Processed_Data2.xlsx', engine='xlsxwriter')

#The total numbers
for key in data:
    writer_helper(data[key],data[key], sheet_name_in='Values_'+key , writer_engine=writer)



    
#The per Capita numbers
for key in ['MIL', 'GDP', 'EDU', 'HEAL']:
    writer_helper(per_cap[key], data[key], sheet_name_in='Per_Capita_'+key , writer_engine=writer)


#The per GDP numbers
for key in ['MIL', 'EDU', 'HEAL']:
    writer_helper(per_gdp[key], data[key], sheet_name_in='Percent_GDP_'+key , writer_engine=writer)


#The absolute change numbers
for key in ['MIL', 'EDU', 'HEAL']:
    writer_helper(abs_change[key], data[key], sheet_name_in='Delta_ABS_'+key , writer_engine=writer)


#The percent change numbers
for key in ['MIL', 'EDU', 'HEAL']:
    writer_helper(per_change[key], data[key], sheet_name_in='Delta_PER_'+key , writer_engine=writer)


#Save and close the whole file
#writer.save()

#%%

def df_filter_helper(df_in, parent_df):
    """
    Sorts and selects the top 10 countries for the dataframe inserted
    Selects the top 10 based of the final year's values.
    
    Returns the shortened daaframe
    """

    #Filter by the parent_df's final countries
    parent_filter = parent_df.sort_values(parent_df.columns[-1], ascending=False)
    parent_filter=parent_filter.head(10)
    df_out=df_in[df_in.index.isin(parent_filter.index)]
    
    return df_out

def transform_column_rows(df_in):
    
    df_out = df_in.dropna().reset_index().melt(id_vars='index')
    df_out = df_out.rename(columns={'index':'Country', 'variable':'Years', 'value':key.capitalize()}) 
    
    df_out=df_out.pivot_table(index=['Years'], columns='Country')
    df_out.columns = df_out.columns.droplevel().rename(None)
    df_out = df_out.reset_index().rename(columns={'index':'Years'})
    
    return df_out





##This section only writes in the format that we need for the website

writer = pd.ExcelWriter('Processed_Data3.xlsx', engine='xlsxwriter')

#Writes the table for the global values
for key in ['MIL', 'EDU', 'HEAL']:
    
    #Absolute Volume
    abs_value=abs_change[key].iloc[:,1::].dropna().reset_index().melt(id_vars='index')
    abs_value = abs_value.rename(columns={'index':'Country', 'variable':'Years', 'value':key.capitalize()}) 
    abs_value["Years"]=(abs_value["Years"].astype(int)-1).astype(str)+'-'+abs_value["Years"]

    per_value=per_change[key].iloc[:,1::].dropna().reset_index().melt(id_vars='index')
    per_value = per_value.rename(columns={'index':'Country', 'variable':'Years', 'value':key.capitalize()}) 
    per_value["Years"]=(per_value["Years"].astype(int)-1).astype(str)+'-'+per_value["Years"]
   
    
    #Trends
    trend_abs_value=trend_abs_change[key].iloc[:,1::].dropna().reset_index().melt(id_vars='index')
    trend_abs_value = trend_abs_value.rename(columns={'index':'Country', 'variable':'Years', 'value':key.capitalize()}) 
    trend_abs_value["Years"] = "2011-2017"
    
    trend_per_value=trend_per_change[key].iloc[:,1::].dropna().reset_index().melt(id_vars='index')
    trend_per_value = trend_per_value.rename(columns={'index':'Country', 'variable':'Years', 'value':key.capitalize()}) 
    trend_per_value["Years"] = "2011-2017"   
    
    abs_value2=pd.concat([abs_value,trend_abs_value], ignore_index=True)
    per_value2=pd.concat([ per_value,trend_per_value], ignore_index=True)
    
    
    
    value=abs_value2.merge(per_value2, on=['Country','Years'])
    value.to_excel(writer, sheet_name='Global_'+key , index=False)


    del abs_value, per_value, trend_per_value, abs_value2, per_value2
    
    
    #
    # This is the overall spending Dashboard
    #
    
    abs_spend = df_filter_helper(data[key], data[key])
    abs_spend = transform_column_rows(abs_spend)
    abs_spend["Type"] = 'Absolute'
    
    cap_spend = df_filter_helper(per_cap[key], data[key])
    cap_spend = transform_column_rows(cap_spend)
    cap_spend["Type"] = 'Per Capita'
    
    gdp_spend = df_filter_helper(per_gdp[key], data[key])
    gdp_spend = transform_column_rows(gdp_spend)
    gdp_spend["Type"] = 'Percent GDP'
    
    
    spend_dash = pd.concat([abs_spend, cap_spend,gdp_spend]).reset_index(drop=True)
    spend_dash = pd.concat([spend_dash.iloc[:,-1],spend_dash.iloc[:,0:-1] ],axis=1,)
    
    spend_dash.to_excel(writer, sheet_name='Dashboard_'+key , index=False)
    
    del abs_spend, cap_spend, gdp_spend
    

    #
    ## Now the Health vs Military Spending
    #
    
    mil_spend = df_filter_helper(data['MIL'], data[key])
    
    mil_spend = mil_spend.dropna().reset_index().melt(id_vars='index')
    mil_spend = mil_spend.rename(columns={'index':'Country', 'variable':'Years', 'value':'Military'}) 
    mil_spend["Labels"]=mil_spend["Country"]+' '+mil_spend["Years"].reset_index(drop=True)
    mil_spend = pd.concat([mil_spend.iloc[:,-1],mil_spend.iloc[:,0:-1] ],axis=1,)
    
    
    var_spend = df_filter_helper(data[key], data[key])
    
    var_spend = var_spend.dropna().reset_index().melt(id_vars='index')
    var_spend = var_spend.rename(columns={'index':'Country', 'variable':'Years', 'value':key.capitalize()}) 
    
    
    mil_stacked=mil_spend.merge(var_spend, on=['Country','Years'])
    mil_stacked.to_excel(writer, sheet_name='MIL_'+key , index=False)
    
    del mil_spend, var_spend
    
    
    
    
    #
    # This is the overall spending Dashboard
    #
    
    bubble_gdp = df_filter_helper(per_cap["GDP"], data[key])
    bubble_gdp = bubble_gdp.dropna().reset_index().melt(id_vars='index')
    bubble_gdp = bubble_gdp.rename(columns={'index':'Country', 'variable':'Years', 'value':'GDP per Capita'}) 
    
    
    
    bubble_var = df_filter_helper(per_cap[key], data[key])
    bubble_var = bubble_var.dropna().reset_index().melt(id_vars='index')
    bubble_var = bubble_var.rename(columns={'index':'Country', 'variable':'Years', 'value':key.capitalize()}) 
    bubble_var['Size'] = 1
    
    bubble_out=pd.concat([bubble_var.Years,bubble_gdp['GDP per Capita'], bubble_var[key.capitalize()],
               bubble_gdp['Country'],bubble_var['Size'], bubble_var['Years'].astype(int)  ], axis=1)
    
    bubble_out.to_excel(writer, sheet_name='Bubble_'+key, index=False )
    
    del bubble_gdp,bubble_var
        

    
    #
    #Absolute Volume
    #
    
    abs_value = df_filter_helper(abs_change[key], data[key]).iloc[:,1::]
    abs_value = transform_column_rows(abs_value)
    abs_value["Type"] = 'Absolute Change'
    
    
    per_value = df_filter_helper(per_change[key], data[key]).iloc[:,1::]
    per_value = transform_column_rows(per_value)
    per_value["Type"] = 'Percent Change'
       
    line_plot = pd.concat([abs_value, per_value]).reset_index(drop=True)
    line_plot = pd.concat([line_plot.iloc[:,-1],line_plot.iloc[:,0:-1] ],axis=1,)
    
    line_plot.to_excel(writer, sheet_name='Line_Change_'+key , index=False)
    
    del abs_value, per_value
    
    
    
#Save and close the whole file
writer.save()
    


    