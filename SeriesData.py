# Written by Ata Coskun
# It gets the datas from bloomberg url and write into a html web page and update it per 30 second according to new datas from url

#!/bin/python3

import sys
import math
import urllib
import json
import datetime
import time

import requests

def read_Data():

    link = "http://www.bloomberght.com/piyasa/intradaydata/dolar"
    data = requests.get(link)
    lastProduct =[]
    seriesData = data.json()['SeriesData'] # get array from url
    i = 0
    while i < len(seriesData)-1 :
        arrangedData =[]
        arrangedData.append(seriesData[i][0]) # get time stamp
        arrangedData.append (datetime.datetime.fromtimestamp(int(seriesData[i][0]) /1000.0).strftime('%Y-%m-%d %H:%M:%S') ) # get date
        arrangedData.append(seriesData[i][1]) # get exchange rate
        lastProduct.append(arrangedData)
        i += 1

    return lastProduct

def createHtmlFile(data):
    html_str = """
<html> 
<head>
<meta http-equiv="refresh" content="5">
<style>
table, th, td {
border: 1px solid black;
}
</style>
</head>
<body>
<h2>Dollar/TL Currency Table</h2>
<table style="width:100%">
    <tr>
       <th>Timestamps</th> 
       <th>Time</th>
       <th>ExchangeRate</th>
    </tr>"""
    part2="""
    <tr>
      <td>{}</td>
      <td>{}</td>
      <td>{}</td>
    </tr>"""
    part3="""
</table>
</body>
</html>"""
    i = len(data)-1
    while i >=0:
       data_str = part2.format(str(data[i][0]),str(data[i][1]),str(data[i][2]))
       html_str = html_str+data_str
       i -= 1
    html_str += part3
    Html_file= open("ExchangeRates.html","w")
    Html_file.write(html_str)
    Html_file.close()
if __name__ == "__main__":

        starttime=time.time()
        while True:
            data = read_Data()
            createHtmlFile(data)
            time.sleep(30.0 - ((time.time() - starttime) % 30.0))

