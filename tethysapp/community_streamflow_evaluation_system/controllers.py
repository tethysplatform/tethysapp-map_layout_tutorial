import json
from pathlib import Path
import pandas as pd
import geopandas as gpd

from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import CSES as app

#functions to load AWS data
import boto3
import os
from botocore import UNSIGNED 
from botocore.client import Config
import os
os.environ['AWS_NO_SIGN_REQUEST'] = 'YES'


#Date picker
from tethys_sdk.gizmos import DatePicker
from django.shortcuts import render, reverse, redirect
from tethys_sdk.gizmos import DatePicker, SelectInput, TextInput
import datetime
from django.http import JsonResponse
from django.urls import reverse_lazy
from datetime import datetime
from datetime import date, timedelta

#Connect web pages
from django.http import HttpResponse 

#utils
from .utils import combine_jsons, reach_json

#Set Global Variables
try:
    ACCESS_KEY_ID = app.get_custom_setting('Access_key_ID')
    ACCESS_KEY_SECRET = app.get_custom_setting('Secret_access_key')
except Exception:
    ACCESS_KEY_ID = ''
    ACCESS_KEY_SECRET = ''

#AWS Data Connectivity
#start session
SESSION = boto3.Session(
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_KEY_SECRET
)
s3 = SESSION.resource('s3')

BUCKET_NAME = 'streamflow-app-data'
BUCKET = s3.Bucket(BUCKET_NAME) 
S3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))

#Controller base configurations
BASEMAPS = [
        {'ESRI': {'layer':'NatGeo_World_Map'}},
        {'ESRI': {'layer':'World_Street_Map'}},
        {'ESRI': {'layer':'World_Imagery'}},
        {'ESRI': {'layer':'World_Shaded_Relief'}},
        {'ESRI': {'layer':'World_Topo_Map'}},
        'OpenStreetMap',      
    ]
MAX_ZOOM = 16
MIN_ZOOM = 1
BACK_URL = reverse_lazy('community_streamflow_evaluation_system:home')

@controller
def home(request):

        start_date_picker = DatePicker( 
            name='start-date',
            display_text='Start Date',
            autoclose=False,
            format='mm-dd-yyyy',
            start_date='01-01-1980',
            end_date= '12-30-2020',
            start_view='year', 
            today_button=False, 
            initial='01-01-2019'
        ) 
     

        context = { 
           'start_date_picker': start_date_picker    
        }


        return render(request, 'community_streamflow_evaluation_system/home.html', context)