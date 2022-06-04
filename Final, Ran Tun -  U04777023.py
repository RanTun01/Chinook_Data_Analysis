#!/usr/bin/env python
# coding: utf-8

# In[463]:


import sqlite3
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
connection = sqlite3.connect("chinook")
def create_connection(path):
    connection = None
    try:
            connection = sqlite3.connect(path)
            print("Connected")
    except error1 as e1:
            print(" '{e1}' Failed to Connect")
    return connection
def execute_read_query(connection,query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except error as e:
        print(f"The Error '{e}' occurred.")
connection = create_connection(r"C:\Users\rannt\Downloads\chinook.db")


# In[464]:


promotion = 'select distinct(SupportRepId) as EmployeeId, e.FirstName as EmployeeFirstName, e.lastname as EmployeeLastName, count(invoiceid) as NumberOfSales,round(AVG(i.total),2) as AvgSale,round(Sum(i.total),2) as TotalSale, round(((count(invoiceid)) + (round(AVG(i.total),2)) + (round(Sum(i.total),2))),2) as EmployeeTotal from customers as c inner join employees as e inner join invoices as i on c.SupportRepId = e.EmployeeId and c.CustomerId = i.CustomerId group by SupportRepId'
cursor = connection.cursor()
cursor.execute(promotion)
promoresult = cursor.fetchall()
for r in promoresult:
    print(r)
pandapromo=execute_read_query(connection, promotion)
promo_df = pd.DataFrame(data = pandapromo, columns = ['EmployeeId','EmployeeFirstName','EmployeeLastName','NumberOfSales','AvgSale','TotalSale', 'EmployeeTotal'])
print(promo_df)
print("Promote Employee:")
print(promo_df.iloc[promo_df['EmployeeTotal'].idxmax()])


# In[475]:


datedata = 'select CustomerId, InvoiceDate from invoices order by CustomerId'
cursor = connection.cursor()
cursor.execute(datedata)
dataresult = cursor.fetchall()
pandadate=execute_read_query(connection, datedata)
customer_df = pd.DataFrame(data = pandadate, columns = ['CustomerId','InvoiceDate'])
customer_df['InvoiceDate'] = pd.to_datetime(customer_df['InvoiceDate'], infer_datetime_format=True)
customer_df['time_to_previous'] = customer_df.groupby('CustomerId')['InvoiceDate'].diff()
customer_df['time_to_previous'] = customer_df['time_to_previous'].dt.days
b = plt.hist(customer_df['time_to_previous'],bins = 3, color= 'Black')


# In[466]:


countrydata= 'select Country,count(distinct(c.CustomerId)) as NumCustomers, round(sum(total),2) as TotalSales, round(round(sum(total),2)/count(distinct(c.CustomerId)),2) as SalePerCapita from customers as c inner join invoices as i on c.customerid = i.customerid group by Country order by SalePerCapita desc'
cursor = connection.cursor()
cursor.execute(countrydata)
country_data = cursor.fetchall()
pandacountry=execute_read_query(connection, countrydata)
country_df = pd.DataFrame(data = pandacountry, columns = ['Country','NumCustomers','TotalSales','SalePerCapita'])
print("Ranked Country Spending per Capita")
print(country_df)


# In[470]:


genredata= 'select g.Name as Genre, round(sum(total),2) as Sales from genres as g inner join tracks as t inner join invoice_items as n inner join invoices as i inner join customers as c on g.GenreId = t.GenreId and t.TrackId = n.TrackId and n.InvoiceId = i.InvoiceId and i.CustomerId = c.CustomerId where Country = \'USA\' group by g.Name order by Sales desc limit 10'
cursor = connection.cursor()
cursor.execute(genredata)
genre_data = cursor.fetchall()
pandagenre=execute_read_query(connection, genredata)
genre_df = pd.DataFrame(data = pandagenre, columns = ['Genre','Sales'])
print('Top 10 Genres in USA are:')
print(genre_df)


# In[468]:


trackdata= 'SELECT substring(t.Name,1, 10) as Name, substring(t.composer, 1,10) as Composer, substring(a.Title,1, 10) as Title, count(t.trackId) AS PlaylistApperance, round(sum(total), 2) AS SumOfSales, round((round(sum(total),2)/count(t.trackId)),2) SalesPerPlaylistApperance FROM playlists AS p INNER JOIN playlist_track AS pt INNER JOIN tracks AS t INNER JOIN invoice_items AS n INNER JOIN invoices AS i INNER JOIN albums AS a ON p.PlaylistId = pt.PlaylistId AND pt.TrackId = t.TrackId AND n.TrackId = t.TrackId AND n.InvoiceId = i.InvoiceId AND t.albumid = a.albumid WHERE composer NOT NULL AND a.Title NOT NULL GROUP BY t.Name ORDER BY SumOfSales DESC LIMIT 50'
cursor = connection.cursor()
cursor.execute(trackdata)
track_data = cursor.fetchall()
pandatrack = execute_read_query(connection, trackdata)
track_df = pd.DataFrame(data = pandatrack, columns = ['Name','Composer','Title','TrackPlaylistApperance','SumOfSales','SalesPerPlaylistApperance'])
print("Top 50 Songs By You:")
print(track_df)

