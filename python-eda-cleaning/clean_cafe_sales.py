import numpy as np 
import pandas as pd 

cafe_sales = pd.read_csv('dirty_cafe_sales.csv') #read csv file into program
print(cafe_sales.head()) #show top 5 entries with headers
print(cafe_sales.tail()) #show last 5 entries with headers

print(cafe_sales.shape) #print shape of df, ie number of rows and columns 

print(cafe_sales.columns) #print header for each column
print(cafe_sales.dtypes) #print dtypes for each column

print(cafe_sales.info()) #shows info for df - columns, number of non-null values per column
#   and dtype of each column 
print('-------------------------------------------------\n') #just to space out info
print(cafe_sales.describe()) #more in depth info about df


#DEALING WITH MISSING VALUES

print('-------------------------------------------------\n') #just to space out info

missing_counts = cafe_sales.isnull().sum()
print(missing_counts) #shows number of null values in each column 

total_cells = np.prod(cafe_sales.shape) #finds total number of cells 
total_missing = missing_counts.sum()

percent_missing = (total_missing / total_cells) * 100
print(percent_missing) #gives the percent of missing values in the df

'''dropped_sales = cafe_sales.dropna()
print(dropped_sales[:20])
print(dropped_sales.shape)
'''
#lose over half the rows using dropna on the whole dataset, so we need to be smarter about this

print(cafe_sales['Item'].unique()) #creates a list containing each unique entry in the Series
print(cafe_sales['Item'].value_counts()) #creates a list that tells us how many time each value appears in the Series
print(cafe_sales['Item'].isnull().sum()) #number of NaN values in Series
#can use above 3 lines to check if Item column no longer contains NaN, UNKNOWN or ERROR

cafe_sales = cafe_sales[cafe_sales.Item.notnull()] #keeps all non-null values
cafe_sales = cafe_sales[cafe_sales.Item != 'UNKNOWN'] #keeps all values that aren't 'UNKNOWN'
cafe_sales = cafe_sales[cafe_sales.Item != 'ERROR'] #keeps all values that aren't 'ERROR'
print(cafe_sales[:20]) #should now have a completely clean 'Item' column

print(cafe_sales['Quantity'].unique())
print(cafe_sales['Price Per Unit'].unique())
print(cafe_sales['Total Spent'].unique())
#shows unique values in the three specified columns

cafe_sales = cafe_sales.replace(to_replace='ERROR', value = np.nan) #replace ERROR and UNKNOWN values with np.nan
cafe_sales = cafe_sales.replace(to_replace='UNKNOWN', value = np.nan)

cafe_sales['Quantity'] = cafe_sales['Quantity'].fillna(0) #fill np.nan values with 0 across three columns
cafe_sales['Price Per Unit'] = cafe_sales['Price Per Unit'].fillna(0)
cafe_sales['Total Spent'] = cafe_sales['Total Spent'].fillna(0)

cafe_sales['Quantity'] = cafe_sales['Quantity'].astype('float64') #change data type for 3 columns
cafe_sales['Price Per Unit'] = cafe_sales['Price Per Unit'].astype('float64') #primarily for dtype of these columns to match np.nan dtype
cafe_sales['Total Spent'] = cafe_sales['Total Spent'].astype('float64')

for index, sale in cafe_sales.iterrows():
    if sale.loc['Price Per Unit'] == 0:
        if sale['Item'] == 'Coffee':
            sale['Price Per Unit'] = 2.0
        if sale['Item'] == 'Cake':
            sale['Price Per Unit'] = 3.0
        if sale['Item'] == 'Cookie':
            sale['Price Per Unit'] = 1.0
        if sale['Item'] == 'Salad':
            sale['Price Per Unit'] = 5.0
        if sale['Item'] == 'Smoothie':
            sale['Price Per Unit'] = 4.0
        if sale['Item'] == 'Sandwich':
            sale['Price Per Unit'] = 8.0
        if sale['Item'] == 'Juice':
            sale['Price Per Unit'] = 3.0
        if sale['Item'] == 'Tea':
            sale['Price Per Unit'] = 1.5

    if sale.loc['Quantity'] == 0:
        sale.loc['Quantity'] = sale.loc['Total Spent'] / sale.loc['Price Per Unit']
    
    if sale['Total Spent'] == 0:
        sale.loc['Total Spent'] = sale.loc['Quantity'] * sale.loc['Price Per Unit']
        
#the above code changes any missing values in Price Per Unit to match the item in the Item column
#  as the prices are fixed for an item 
#I then loop through the Quantity and Total Spent columns and apply some basic maths concepts to
# solve any missing values for what they should be 
#this primarily works as there is a singular item per transaction ID - otherwise it would be more complex 



cafe_sales = cafe_sales[cafe_sales['Transaction Date'].notnull()]
cafe_sales['Transaction Date'] = pd.to_datetime(cafe_sales['Transaction Date'], format='%Y-%m-%d', errors='coerce')

date_sort = cafe_sales.sort_values(by='Transaction Date') #sort df by date but set it under a new name
print(date_sort[:10]) #used to check that all NaT values had been removed from df
print(date_sort[-10:])


missing_counts = cafe_sales.isnull().sum() #confirmation there are now no errors in Quantity, Price Per Unit and Total Spent
print(missing_counts)
