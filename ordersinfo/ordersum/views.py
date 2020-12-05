from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import random

# Create your views here.

def home(request):
    #Reading files
    orderMain = pd.read_excel('ordersinfo/Sample_Orders_Data.xls',sheet_name='Order Main')
    customerMaster = pd.read_excel('ordersinfo/Sample_Orders_Data.xls',sheet_name='Customer Main')
    #Formatting Customer Master Table
    customerMaster['Address'] = customerMaster['City']+', '+customerMaster['State']+' '+customerMaster['Postal Code'].astype(str)+', '+customerMaster['Country/Region']
    customerMaster.drop(['City','State','Postal Code','Country/Region'],axis=1,inplace=True)
    #Generating Phone Numbers & Adding to Customer Master Table
    phoneNum = []
    def gen_phone():
        first = str(random.randint(100,999))
        second = str(random.randint(1,888)).zfill(3)
        last = (str(random.randint(1,9998)).zfill(4))
        while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
            last = (str(random.randint(1,9998)).zfill(4))
        return '{}-{}-{}'.format(first,second, last)
    for i in range(0,47):
        phone = gen_phone()
        phoneNum.append(phone)
    customerMaster['Phone Numbers'] = phoneNum
    #Merging Order Main & Customer Master Table
    orderCustomer = pd.merge(orderMain,customerMaster,on='Customer ID')
    #Getting Customer Names To Add to Drop-Down List
    customers = orderCustomer['Customer Name'].tolist()
    customers = list(set(customers))
    customers.sort()
    context = {'customers':customers}

    return render(request,'ordersum/dashboard.html',context)

def namedata(request):
    #Reading files
    orderMain = pd.read_excel('ordersinfo/Sample_Orders_Data.xls',sheet_name='Order Main')
    customerMaster = pd.read_excel('ordersinfo/Sample_Orders_Data.xls',sheet_name='Customer Main')
    #Formatting Customer Master Table
    customerMaster['Address'] = customerMaster['City']+', '+customerMaster['State']+' '+customerMaster['Postal Code'].astype(str)+', '+customerMaster['Country/Region']
    customerMaster.drop(['City','State','Postal Code','Country/Region'],axis=1,inplace=True)
    #Generating Phone Numbers & Adding to Customer Master Table
    phoneNum = []
    def gen_phone():
        first = str(random.randint(100,999))
        second = str(random.randint(1,888)).zfill(3)
        last = (str(random.randint(1,9998)).zfill(4))
        while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
            last = (str(random.randint(1,9998)).zfill(4))
        return '{}-{}-{}'.format(first,second, last)
    for i in range(0,47):
        phone = gen_phone()
        phoneNum.append(phone)
    customerMaster['Phone Numbers'] = phoneNum
    #Merging Order Main & Customer Master Table
    orderCustomer = pd.merge(orderMain,customerMaster,on='Customer ID')
    #Get Selected Customer Name
    if request.method == "POST":
        customerName = request.POST['drop1']
    #Data For Selected Customer
    cust = orderCustomer[orderCustomer['Customer Name']==customerName].copy()
    totalSpent = np.around(cust['Item Price'].sum(),2)
    address = cust['Address'].unique()[0]
    phonenumber = cust['Phone Numbers'].unique()[0]
    data = cust[['Order Date','Item Price','Status']].groupby('Order Date').sum()
    dates = data.index.tolist()
    price = data.values.tolist()
    status = cust['Status'].values.tolist()
    customers = customerMaster['Customer Name'].tolist()
    customers.sort()
    #Table Data

    table_content = cust[['Order ID','Order Date','Item Name','Item Price','Status']].to_html(index=None)
    context = {'customers':customers,'spent':totalSpent,'customerName':customerName,'address':address,'phonenumber':phonenumber,'dates':dates,'price':price,'status':status,'table_content':table_content}
    return render(request,'ordersum/dashboard.html',context)
