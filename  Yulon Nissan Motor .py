#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 14:22:37 2023

@author: wangshuyou
"""

import googlemaps
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# googlemap_API
gmaps=googlemaps.Client(key='') # API key
cities= ["臺北市","新北市","桃園市","臺中市","臺南市","高雄市","基隆市","新竹市","嘉義市",
         "新竹縣","苗栗縣","彰化縣","南投縣","雲林縣","嘉義縣","屏東縣","宜蘭縣","花蓮縣"]

###############################################################################
# 資料搜集--量販店、國中小、露營點
# 1. 取得量販店經緯度
results = []
stores = []
# Geocoding an address
for city in cities:
    geocode_result = gmaps.geocode(city)
    loc = geocode_result[0]['geometry']['location']
    query_result = gmaps.places_nearby(type ="supermarket",location=loc, radius=100000)
#    for i in range(len(query_result['results'])):
#        results.append(query_result['results'][i]['geometry']['location'])
    markets = []
    for i in range(len(query_result['results'])):
        choice = query_result['results'][i]['name']
        if 'Carrefour' in choice:
            markets.append(query_result['results'][i]['geometry']['location'])
            markets.append(choice)
            print(choice)
        elif '好市多' in choice:
            markets.append(query_result['results'][i]['geometry']['location'])
            markets.append(choice)
            print(choice)
        elif '大潤發' in choice:
            markets.append(query_result['results'][i]['geometry']['location'])
            markets.append(choice)
            print(choice)
        elif '愛買' in choice:
            markets.append(query_result['results'][i]['geometry']['location'])
            markets.append(choice)
            print(choice)         
markets.to_csv('markets.csv')

# 2. 婦產科經緯度
results = []
for city in cities:
    geocode_result = gmaps.geocode(city)
    loc = geocode_result[0]['geometry']['location']
    query_result = gmaps.places_nearby(keyword = '婦產科',location=loc, radius=1000000)
    for i in range(len(query_result['results'])):
        if '婦產科' in query_result['results'][i]['name']:
            results.append(query_result['results'][i]['geometry']['location'])
# 看各地區婦產科家數
OG = []
for city in cities:
    results = []
    # Geocoding an address
    geocode_result = gmaps.geocode('cities')
    loc = geocode_result[0]['geometry']['location']
    query_result = gmaps.places_nearby(keyword="婦產科",location=loc, radius=10000)
    results.extend(query_result['results'])
    while query_result.get('next_page_token'):
        time.sleep(2)
        query_result = gmaps.places_nearby(page_token=query_result['next_page_token'])
        results.extend(query_result['results'])    
    print("找到以"+city+"為中心半徑10000公尺的婦產科數量(google mapi api上限提供60間): "+str(len(results)))
    for place in results:
        OG.append(place['place_id'])   
OG.to_csv('OG.csv')

# 3. 國中小經緯度
results = []
for city in cities:
    geocode_result = gmaps.geocode(city)
    loc = geocode_result[0]['geometry']['location']
    query_result = gmaps.places_nearby(keyword="小學",location=loc, radius=10000)
    for i in range(len(query_result['results'])):
        if '小學' in query_result['results'][i]['name']:
            results.append(query_result['results'][i]['geometry']['location'])
        elif 'Elementary School' in query_result['results'][i]['name']:
            results.append(query_result['results'][i]['geometry']['location'])
        elif '國小' in query_result['results'][i]['name']:
            results.append(query_result['results'][i]['geometry']['location'])
# 看各地區小學家數
ids = []
for city in cities:
    results = []
    # Geocoding an address
    geocode_result = gmaps.geocode(city)
    loc = geocode_result[0]['geometry']['location']
    query_result = gmaps.places_nearby(keyword="小學",location=loc, radius=10000)
    results.extend(query_result['results'])
    while query_result.get('next_page_token'):
        time.sleep(2)
        query_result = gmaps.places_nearby(page_token=query_result['next_page_token'])
        results.extend(query_result['results']) # 追加list    
    print("找到以"+city+"為中心半徑10000公尺的小學數量(google mapi api上限提供60間): "+str(len(results)))
    for place in results:
        ids.append(place['place_id'])


lat = []
for i in results:
    lat.append(i['lat'])
lon = []
for i in results:
    lon.append(i['lng']) 
lat = pd.DataFrame(lat)
lon = pd.DataFrame(lon)

ele = pd.concat([lat,lon],axis =1)
ele = ele.set_axis(['lat','lon'],axis =1)
ele.to_csv('ele.csv')

###############################################################################
# 停靠點標記
# 匯入資料
df = pd.read_csv('stop_loc.csv',low_memory=False)
tw = pd.read_csv('Taiwan_polygons.csv') #外部資料
camp = pd.read_csv('campground.csv') #外部資料

# 排除（少資料）離島、定位點奇怪的位置
OG = OG.set_axis(['lat','lon'],axis = 1)
camp = camp.set_axis(['name','lat','lon'], axis =1)
len(OG)
camp = camp[camp['lon'] >= 119.9]
len(camp)
markets = markets[markets['lon'] >= 118.5]
markets = markets.set_axis(['種類','地址','lat','lon','location'], axis =1)
len(markets)
markets['location'] = markets['地址'].str[:3]
df['datetime'] = pd.to_datetime(df['datetime'])
df['dtime'] = df[['deviceid','datetime']].groupby('deviceid').shift(1)
df['time_diff'] = df['datetime']-df['dtime']
df = df[(df['f3d'] == True)]
df = df[df['cond'] != '澎湖縣']
print(df.head())

# 確認非等紅綠燈
df_stop = df[df['time_diff'] >= '00:03:00']
df_stop = df_stop.drop_duplicates()
stop_lat = list(df_stop['lat.x'])
stop_lon = list(df_stop['lon.x'])

# 確認有沒有0
zero_t = []
for index,i in enumerate(stop_lat):
    if i < 5:
        #print(index,i)
        zero_t.append(index)
print(len(zero_t))
print(zero_t)

for ind,i in enumerate(stop_lat):
    if i > 26.0:
        print(ind,i)

df_stop = df_stop.assign(school=False,school_name = np.NaN, school_lat = np.NaN,school_lon = np.NaN,
                         Obstetrics_Gynecology=False, Obstetrics_Gynecology_lat = np.NaN,Obstetrics_Gynecology_lon = np.NaN,
                        market = False,market_name = np.NaN,market_lat = np.NaN,market_lon = np.NaN)

plt.scatter(x = ele['lon'], y = ele['lat'], s = 0.5)
plt.show()

plt.scatter(x = tw['lon'], y = tw['lat'], s = 0.5)
plt.scatter(x = stop_lon, y = stop_lat, s = 0.5)
plt.scatter(x = ele['lon'], y = ele['lat'], c = 'black', s = 0.5)
plt.show()

# 經緯度歐式距離換算公尺
def rad2deg(radians):
    degrees = radians * 180 / np.pi
    return degrees
def deg2rad(degrees):
    radians = degrees * np.pi / 180
    return radians
# 兩點距離換算
def getDistanceBetweenPointsNew(latitude1, longitude1, latitude2, longitude2, unit = 'meters'):
    theta = longitude1 - longitude2    
    distance = 60 * 1.1515 * rad2deg(
        np.arccos(
            (np.sin(deg2rad(latitude1)) * np.sin(deg2rad(latitude2))) + 
            (np.cos(deg2rad(latitude1)) * np.cos(deg2rad(latitude2)) * np.cos(deg2rad(theta)))
        )
    )
    
    if unit == 'miles':
        return round(distance, 2)
    if unit == 'kilometers':
        return round(distance * 1.609, 2)
    if unit == 'meters':
        return round(distance *1.609 * 1000, 2)
    
# 計算停靠點附近300公尺是否有國中小
start = time.time()
cond = []
for i in range(len(ele)):
    for j in range(len(df_stop)):
        if (ele['縣市別'].iloc[i] == df_stop['cond'].iloc[j]) and (df_stop['school'].iloc[j] == False) and (df_stop['datetime'].iloc[j].hour >= 7 and df_stop['datetime'].iloc[j].hour <= 18)and (df_stop['datetime'].iloc[j].weekday() < 5 ):# 5 : Saturday
            jug = getDistanceBetweenPointsNew(df_stop['lat.x'].iloc[j],df_stop['lon.x'].iloc[j], ele['lat'].iloc[i],ele['lon'].iloc[i])
            cond.append(jug)
            if jug <= 300:
                df_stop['school'].iloc[j] = 'True'
                df_stop['school_name'].iloc[j] = ele['學校名稱'].iloc[i]
                df_stop['school_lat'].iloc[j] = ele['lat'].iloc[i]
                df_stop['school_lon'].iloc[j] = ele['lon'].iloc[i]
end = time.time()
print(f'執行秒數:{end - start}')

plt.scatter(x = tw['lon'], y = tw['lat'], s = 0.5)
plt.scatter(x = stop_lon, y = stop_lat, s = 0.5)
plt.scatter(x = OG['lon'], y = OG['lat'], c = 'black', s = 0.5)
plt.show()

# 計算停靠點附近500公尺是否有婦產科
start = time.time()
cond_og = []
for i in range(len(OG)):
    for j in range(len(df_stop)):
        if (df_stop['Obstetrics_Gynecology'].iloc[j] == False):
            jug = getDistanceBetweenPointsNew(df_stop['lat.x'].iloc[j],df_stop['lon.x'].iloc[j], OG['lat'].iloc[i],OG['lon'].iloc[i])
            cond_og.append(jug)
            if jug <= 500:
                df_stop['Obstetrics_Gynecology'].iloc[j] = 'True'
                df_stop['Obstetrics_Gynecology_lat'].iloc[j] = OG['lat'].iloc[i]
                df_stop['Obstetrics_Gynecology_lon'].iloc[j] = OG['lon'].iloc[i]
end = time.time()
print(f'執行秒數:{end - start}')

plt.scatter(x = tw['lon'], y = tw['lat'], s = 0.5)
plt.scatter(x = stop_lon, y = stop_lat, s = 0.5)
plt.scatter(x = markets['lon'], y = markets['lat'], c = 'black', s = 0.5)
plt.show()

# 計算停靠點附近200公尺是否有量販店
start = time.time()
cond = []
for i in range(len(markets)):
    for j in range(len(df_stop)):
        if (markets['location'].iloc[i] == df_stop['cond'].iloc[j]) and (df_stop['market'].iloc[j] == False) :
            jug = getDistanceBetweenPointsNew(df_stop['lat.x'].iloc[j],df_stop['lon.x'].iloc[j], markets['lat'].iloc[i],markets['lon'].iloc[i])
            cond.append(jug)
            if jug <= 200:
                df_stop['market'].iloc[j] = 'True'
                df_stop['market_name'].iloc[j] = markets['種類'].iloc[i]
                df_stop['market_lat'].iloc[j] = markets['lat'].iloc[i]
                df_stop['market_lon'].iloc[j] = markets['lon'].iloc[i]
end = time.time()
print(f'執行秒數:{end - start}')

# 計算停靠點附近200公尺是否有露營點
start = time.time()
cond = []
for i in range(len(camp)):
    for j in range(len(df_stop)):
        if df_stop['camp'].iloc[j] == False :
            jug = getDistanceBetweenPointsNew(df_stop['lat.x'].iloc[j],df_stop['lon.x'].iloc[j], camp['lat'].iloc[i],camp['lon'].iloc[i])
            cond.append(jug)
            if jug <= 200:
                df_stop['camp'].iloc[j] = 'True'
                df_stop['camp_name'].iloc[j] = camp['name'].iloc[i]
                df_stop['camp_lat'].iloc[j] = camp['lat'].iloc[i]
                df_stop['camp_lon'].iloc[j] = camp['lon'].iloc[i]
end = time.time()
print(f'執行秒數:{end - start}')

plt.scatter(x = tw['lon'], y = tw['lat'], s = 0.5)
plt.scatter(x = stop_lon, y = stop_lat, s = 0.5)
plt.scatter(x = camp['lon'], y = camp['lat'], c = 'black', s = 0.5)
plt.show()