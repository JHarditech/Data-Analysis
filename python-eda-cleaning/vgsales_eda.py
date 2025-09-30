import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

vg_sales = pd.read_csv('vgchartz-2024.csv')

print(vg_sales.head())
print(vg_sales.info())
print(vg_sales.describe())
print(vg_sales.isnull().sum())

vg_sales = vg_sales.drop('img', axis='columns') #img columns isn't necessary for EDA
vg_sales = vg_sales.drop('last_update', axis='columns')

'''plt.figure(figsize=(20,9))
sns.histplot(data=vg_sales, x='genre')
plt.show()'''

#Games released per year
vg_sales['release_date'] = pd.to_datetime(vg_sales['release_date'], format='%Y-%m-%d', errors='coerce')

vg_year = vg_sales.dropna(subset=['release_date'])
vg_year['release_date'] = pd.to_datetime(vg_year['release_date'], format='%Y', errors='coerce')
'''sns.histplot(data=vg_year, x='release_date')
plt.show()'''

vg_year['year'] = vg_year['release_date'].dt.year
vg_year['year'] = vg_year['year'].astype(int)
'''sns.histplot(data=vg_year, x='year')
plt.show()
'''
#testing to see if I could get more values in the total sales column
'''vg_total = vg_sales.fillna(0) 

sum=[]
empty = []
null = []
for index, row in vg_total.iterrows():
    if row.total_sales == 0 and row.na_sales*row.jp_sales*row.pal_sales*row.other_sales != 0:
        row.total_sales = row.na_sales+row.jp_sales+row.pal_sales+row.other_sales
        sum.append(index)

    if row.total_sales==0 and (row.na_sales==0 or row.jp_sales==0 or row.pal_sales==0 or row.other_sales==0):
        null.append(index)

    if row.total_sales == 0:
        empty.append(index)

print(len(empty))
print(len(sum))
print(len(null))
'''

#Video game sales per year
vg_totalsales = vg_sales.dropna(subset='total_sales')
vg_totalsales['release_date'] = pd.to_datetime(vg_year['release_date'], format='%Y', errors='coerce')
vg_totalsales['total_sales'] = vg_totalsales['total_sales'].sort_values(ascending=True)

'''sns.lineplot(data=vg_totalsales, x='release_date', y='total_sales')
plt.show()'''

#Video game sales per genre
genre_unique = vg_totalsales['genre'].unique()
print(len(genre_unique))
vg_totalsales = vg_totalsales.groupby(by='genre')['total_sales'].sum().sort_values(ascending=False)

'''sns.barplot(x=vg_totalsales.index, y=vg_totalsales.values)
plt.show()'''

#Average critic rating per genre
vg_critic = vg_sales.dropna(subset=['critic_score'])
vg_critic = vg_critic.groupby(by='genre')['critic_score'].mean().sort_values(ascending=False)

'''sns.barplot(x=vg_critic.index, y=vg_critic.values, palette='viridis')
plt.ylabel('Mean Critic Rating')
plt.show()'''


#Games per publisher - top 10 publishers
publisher_unique = vg_sales['publisher'].unique()
print(len(publisher_unique))
print(publisher_unique[:50])

'''ea = 0
ms = 0
sony = 0
for index, row in vg_sales.iterrows():
    if 'electronic arts' in row.publisher.lower():
        ea += 1
    if 'EA' in row.publisher:
        ea+=1
    if 'sony' in row.publisher.lower():
        sony += 1
    if 'microsoft' in row.publisher.lower():
        ms+=1
        
print(f"EA: {ea}")
print(f"Microsoft: {ms}")
print(f"Sony: {sony}")'''

ea = []
ms = []
sony = []
for index, row in vg_sales.iterrows():
    if 'electronic arts' in row.publisher.lower():
        ea.append(row.publisher)
    if 'EA' in row.publisher:
        ea.append(row.publisher)
    if 'sony' in row.publisher.lower():
        sony.append(row.publisher)
    if 'microsoft' in row.publisher.lower():
        ms.append(row.publisher)


print(f"EA: {len(ea)}")
print(f"Microsoft: {len(ms)}")
print(f"Sony: {len(sony)}")

ea_unique = []
for item in ea:
    if item not in ea_unique:
        ea_unique.append(item)

print(len(ea_unique))
print(f"EA unique: {ea_unique}")

non_ea = ['TEAM HORAY', 'SCEA Studio San Diego', 'LEANDRO PIM', 'EASY Inc.', 'SCEA','AREA 34, Inc.']
for item in ea_unique:
    if item in non_ea:
        ea_unique.remove(item)

ea_unique.remove('EASY Inc.')
print(f"EA unique: {ea_unique}")

ms_unique = []
for item in ms:
    if item not in ms_unique:
        ms_unique.append(item)

print(len(ms_unique))
print(f"MS unique: {ms_unique}")


sony_unique = []
for item in sony:
    if item not in sony_unique:
        sony_unique.append(item)

print(len(sony_unique))
print(f"Sony unique: {sony_unique}")


vg_pub = vg_sales.dropna(subset='publisher')

pub_unique = vg_pub['publisher'].unique()
print(len(pub_unique))

vg_pub['publisher'] = vg_pub['publisher'].replace(to_replace=ea_unique, value = 'Electronic Arts')
vg_pub['publisher'] = vg_pub['publisher'].replace(to_replace=ms_unique, value = 'Microsoft Game Studios')
vg_pub['publisher'] = vg_pub['publisher'].replace(to_replace=sony_unique, value = 'Sony Entertainment')

pub_unique = vg_pub['publisher'].unique()
print(len(pub_unique))

pub_sales = vg_pub.groupby('publisher')['total_sales'].sum().sort_values(ascending=False).head(10)
'''plt.figure(figsize=(20,10))
sns.barplot(x=pub_sales.index, y=pub_sales.values, palette='viridis')
plt.title('Total Sales for Top 10 Publishers')
plt.xlabel('Publisher')
plt.ylabel('Total Sales (millions)')
plt.xticks(rotation=30)
plt.grid(True)
plt.show()'''


#Heatmap for sales per genre per year 
year_genre = vg_sales.dropna(subset='release_date')
year_genre['release_date'] = pd.to_datetime(year_genre['release_date'], format='%Y', errors='coerce')
year_genre['year'] = year_genre['release_date'].dt.year
print(year_genre['year'].head())
year_genre['year'] = year_genre['year'].astype(int)
genre_year = year_genre.pivot_table(values='total_sales', index='genre', columns='year', 
                                    aggfunc='sum', fill_value=0)

'''plt.figure(figsize=(20,10))
sns.heatmap(genre_year, cmap='coolwarm')
plt.show()'''