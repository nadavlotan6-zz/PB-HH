#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import urllib
import pandas as pd
import time
import math
from flask import Flask
from flask import request

# # TODO: Need to get url as trigger

app = Flask(__name__)
@app.route('/')
def handleExcel():
    EXAMPLE_URL = request.args.get('example')
    print(EXAMPLE_URL)

    # Assign url of file: url
    url = request.args.get('url')
    # url = 'https://pb-import-files.s3-eu-west-1.amazonaws.com/BMBY_export_English.xlsx'
    # url = 'https://pb-import-files.s3-eu-west-1.amazonaws.com/data.xlsx'

    # Read file into a DataFrame and print its head
    df = pd.read_excel(url)

    # Drop Irrelevant Columns
    df = df.drop('Unnamed: 0', axis=1)

    # Transform elevator column -> Change "לא" and blanks to False and "כן" to True
    for idx in df.elevator.index:
        updated_str = df['elevator'][idx]
        encoded = updated_str.encode('utf-8').strip()
        if "לא" in encoded:
            df.at[idx, 'elevator'] = False
        else:
            df.at[idx, 'elevator'] = True

    # Transform air_conditioner column -> Change "לא" and blanks to False and "כן" to True
    for idx in df.air_conditioner.index:
        updated_str = df['air_conditioner'][idx]
        if isinstance(updated_str, unicode):
            encoded = updated_str.encode('utf-8').strip()
            if "לא" in encoded:
                encoded = False
            else:
                encoded = True
        else:
            if math.isnan(updated_str):
                encoded = False
            else:
                encoded = True

    df.at[idx, 'air_conditioner'] = encoded

    # Transform Date Time to the required format
    df.registration_date = df.registration_date.dt.strftime("%d/%m/%y")
    df.last_communication_date = df.last_communication_date.dt.strftime(
        "%d/%m/%y")

    # TODO: Add ownerid
    # Add RECORDTYPEID, OWNERID columns to DataFrame
    # Indicates a "Sell" type
    df.insert(0, 'RECORDTYPEID', '0124J0000001b45QAA')
    df.insert(0, 'OWNERID', '0054J000002DDqo')  # Indicate the default user -

    # TODO: Picklist values - should I change it to English

    # TODO: Get entire API naming convention
    # Change column headers to match PropertyBase convention
    df.rename(columns={'Phone_number': 'PHONENUMBER',
                       'registration_date': 'CREATEDDATE',
                       'air_conditioner': 'AIRCONDITIONER',
                       'address': '	pba__Address_pb__c',
                       'first_name': '	First_Name__c',
                       'family_name': 'Last_Name__c',
                       'last_communication_date': '',
                       'Ctiy': 'pba__City_pb__c',
                       'Nighborhood': 'pba__Neighborhood_pb__c',
                       'additional_phone_number': '	Second_mobile__c',
                       'cellphone_nubmer': 'Mobile__c',
                       'rooms': 'pba__Bedrooms_pb__c',
                       'floor': 'pba__Floor__c',
                       'balcony': '	Balcony__c',
                       #    'action_type': '',
                       'agent': 'Agent__c',
                       'source': 'Source__c',
                       'price': 'pba__ListingPrice_pb__c',
                       #    'price_2': '',
                       'sqaure_meters': 'pba__TotalArea_pb__c',
                       'apartment_type': 'pba__ListingType__c',
                       'elevator': 'Elavator__c',
                       'storage': 'Storage_Area__c',
                       'price_per_meter': 'Price_sq__c',
                       'building_condition': 'pba__Status__c',
                       #    'building_age': '',
                       #    'bmby_id': '',
                       #    'משימה\פגישה אחרונה': '',
                       }, inplace=True)

    # print(df.head())

    print(df.info())

    df.to_excel('output.xlsx')

    return 'Hello world!'
