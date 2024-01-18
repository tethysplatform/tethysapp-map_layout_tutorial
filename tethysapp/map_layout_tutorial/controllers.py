import json
from pathlib import Path
import pandas as pd

from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import MapLayoutTutorial as app

#functions to load AWS data
import boto3
import os
from botocore import UNSIGNED
from botocore.client import Config

#Date picker
from tethys_sdk.gizmos import DatePicker
from django.shortcuts import render
from tethys_sdk.gizmos import DatePicker
import datetime
from django.http import JsonResponse

HOME = os.getcwd()
MODEL_OUTPUT_FOLDER_NAME = 'sample_nextgen_data'
INIT_DATE='1/1/2019' 
END_DATE='6/11/2019'

#Connect to AWS s3 for data
#home = Path(app_workspace.path) #"./workspaces/app_workspace"
KEYPATH = f"{HOME}/tethysapp/map_layout_tutorial/AWSaccessKeys.csv"
ACCESS = pd.read_csv(KEYPATH)
#start session
SESSION = boto3.Session(
    aws_access_key_id=ACCESS['Access key ID'][0],
    aws_secret_access_key=ACCESS['Secret access key'][0],
)
s3 = SESSION.resource('s3')
#AWS bucket information
BUCKET_NAME = 'streamflow-app-data'
BUCKET = s3.Bucket(BUCKET_NAME) 
S3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))


@controller(name="home", app_workspace=True)
class MapLayoutTutorialMap(MapLayout):
    app = app
    base_template = 'map_layout_tutorial/base.html'
    map_title = 'Research Oriented Streamflow Evaluation Toolset'
    map_subtitle = 'An open-source hydrological model evaluation tool for NHDPlus models'
    basemaps = ['OpenStreetMap', 'ESRI']
    default_map_extent = [-87.83371926334216, 33.73443611122197, -86.20833410475134, 34.456557011634175]
    max_zoom = 14
    min_zoom = 9
    show_properties_popup = True
    plot_slide_sheet = True
    template_name = 'map_layout_tutorial/roset_view.html'

    def update_data(self, request, *args, **kwargs):
        """
        Custom REST method for updating data form Map Layout view.
        """
        #  = request.POST
        
        INIT_DATE=request.POST.get('start_date')
        END_DATE=request.POST.get('end_date')

        print(INIT_DATE,END_DATE)
        # Create layer groups
        layer_groups = [
            self.build_layer_group(
                id='nextgen-features',
                display_name='NextGen Features',
                layer_control='checkbox',  # 'checkbox' or 'radio'
                layers=[
                    #catchments_layer
                    
                ]
            )
        ]
        # update the map respectively
        ...
        return JsonResponse({'success': True})


    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs): #can we select the geojson files from the input fields (e.g: AL, or a dropdown)
        """
        Add layers to the MapLayout and create associated layer group objects.
        """
        # data_test = request.GET.get('other')
        # print(data_test)
        # Load GeoJSON from files
        config_directory = Path(app_workspace.path) / MODEL_OUTPUT_FOLDER_NAME / 'config'
        
        ''' Change the below nexus points and catchment files if you want to add them to the app interface
        # Nexus Points
        nexus_path = config_directory / 'nexus_4326.geojson'
        with open(nexus_path) as nf:
            nexus_geojson = json.loads(nf.read())

        nexus_layer = self.build_geojson_layer(
            geojson=nexus_geojson,
            layer_name='nexus',
            layer_title='Nexus',
            layer_variable='nexus',
            visible=True,
            selectable=True,
            plottable=True,
        )

        # Catchments
        
        catchments_path = config_directory / 'catchments_4326.geojson'
        with open(catchments_path) as cf:
            catchments_geojson = json.loads(cf.read())

        catchments_layer = self.build_geojson_layer(
            geojson=catchments_geojson,
            layer_name='catchments',
            layer_title='Catchments',
            layer_variable='catchments',
            visible=True,
            selectable=True,
            plottable=True,
        )
        '''
        # flowpaths - from AWS s3
        #flowpaths_path = 'GeoJSON/AL/flowpaths_4326_AL.geojson'
        #obj = s3.Object(BUCKET_NAME, flowpaths_path)
        #flowpaths_geojson = json.load(obj.get()['Body']) 
        #flowpaths_path = config_directory / 'flowpath_08_1000_4326.geojson'
        flowpaths_path = config_directory / 'flowpaths_4326_AL.geojson'
        with open(flowpaths_path) as ff:
            flowpaths_geojson = json.loads(ff.read())

        flowpaths_layer = self.build_geojson_layer(
            geojson=flowpaths_geojson,
            layer_name='flowpaths',
            layer_title='Flowpaths',
            layer_variable='flowpaths',
            visible=True,
            selectable=True,
            plottable=True,
        )

        # USGS stations - from AWS s3
        stations_path = 'GeoJSON/AL/StreamStats_4326_AL.geojson'
        obj = s3.Object(BUCKET_NAME, stations_path)
        stations_geojson = json.load(obj.get()['Body']) 

        stations_layer = self.build_geojson_layer(
            geojson=stations_geojson,
            layer_name='USGS Stations',
            layer_title='USGS Station',
            layer_variable='stations',
            visible=True,
            selectable=True,
            plottable=True,
        )

        # Create layer groups
        layer_groups = [
            self.build_layer_group(
                id='nextgen-features',
                display_name='NextGen Features',
                layer_control='checkbox',  # 'checkbox' or 'radio'
                layers=[
                    stations_layer,
                    #nexus_layer,
                    flowpaths_layer,
                    #catchments_layer
                    
                ]
            )
        ]
        

        return layer_groups

    @classmethod
    def get_vector_style_map(cls):
        return {
            'Point': {'ol.style.Style': {
                'image': {'ol.style.Circle': {
                    'radius': 5,
                    'fill': {'ol.style.Fill': {
                        'color': 'white',
                    }},
                    'stroke': {'ol.style.Stroke': {
                        'color': 'red',
                        'width': 3
                    }}
                }}
            }},
            'MultiPolygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'navy',
                    'width': 3
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 25, 128, 0.1)'
                }}
            }},
             'MultiLineString': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'navy',
                    'width': 2
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 25, 128, 0.1)'
                }}
            }},
        }

    def get_plot_for_layer_feature(self, request, layer_name, feature_id, layer_data, feature_props, app_workspace,
                                *args, **kwargs):
        """
        Retrieves plot data for given feature on given layer.
        - Can we use this function to plot two streams - explore by adding the example one again but multiplying by a factor (e.g., *1.2)
        Args:
            layer_name (str): Name/id of layer.
            feature_id (str): ID of feature.
            layer_data (dict): The MVLayer.data dictionary.
            feature_props (dict): The properties of the selected feature.

        Returns:
            str, list<dict>, dict: plot title, data series, and layout options, respectively.
      """
        # Get the feature ids
        id = feature_props.get('id') 
        NHD_id = feature_props.get('NHD_id') 
        state = feature_props.get('state')
        #print(id, NHD_id, state)

        '''need to create our own geojson files, likely for usgs sites and nhd reaches 
        3. add all nhdplus reaches (blue lines) for all available nhdplus streams in the HUC 
        '''
        

        # USGS observed flow
        if layer_name == 'USGS Stations':
            layout = {
                'yaxis': {
                    'title': 'Streamflow (cfs)'
                } 
            }
            #output directory for AWS
            #USGS observed flow
            USGS_directory = f"NWIS/NWIS_sites_{state}.h5/NWIS_{id}.csv"
            obj = BUCKET.Object(USGS_directory)
            body = obj.get()['Body']
            USGS_df = pd.read_csv(body)
            USGS_df.pop('Unnamed: 0')    

            #modeled flow, starting with NWM
            self.model = 'NWM_v2.1'
            #NHD_id = '19626108'
            model_directory = f"{self.model}/NHD_segments_{state}.h5/{self.model}_{NHD_id}.csv"  #put state in geojson file
            obj = BUCKET.Object(model_directory)
            body = obj.get()['Body']
            model_df = pd.read_csv(body)
            model_df.pop('Unnamed: 0')

            #combine Dfs, remove nans
            USGS_df.drop_duplicates(subset=['Datetime'], inplace=True)
            model_df.drop_duplicates(subset=['Datetime'],  inplace=True)
            #align by index
            USGS_df.set_index('Datetime', inplace = True)
            model_df.set_index('Datetime', inplace = True)
            DF = pd.concat([USGS_df, model_df], axis = 1, join = 'inner')
            DF.reset_index(inplace=True)


            #put USGS and modeled streamflows together
            time_col = DF.Datetime.to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)
            USGS_streamflow_cfs = DF.USGS_flow.to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)
            Mod_streamflow_cfs = DF[f"{self.model[:3]}_flow"].to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)
            #print('USGS', USGS_streamflow_cfs)
            #print('NWM', Mod_streamflow_cfs)


            data = [
                {
                    'name': 'USGS Observed',
                    'mode': 'lines',
                    'x': time_col,
                    'y': USGS_streamflow_cfs,
                    'line': {
                        'width': 2,
                        'color': 'blue'
                    }
                },
                {
                    'name': f"{self.model} Modeled",
                    'mode': 'lines',
                    'x': time_col,
                    'y': Mod_streamflow_cfs,
                    'line': {
                        'width': 2,
                        'color': 'red'
                    }
                },
            ]


            return f'{self.model} Modeled and Observed Streamflow at USGS site: "{id}"', data, layout

        # Catchments
        '''
        if layer_name == 'catchments':
            layout = {
                'yaxis': {
                    'title': 'Evapotranspiration (mm/hr)'
                }
            }

            output_path = output_directory / f'{id}.csv'
            if not output_path.exists():
                print(f'WARNING: no such file {output_path}')
                return f'No Data Found for Catchment "{id}"', [], layout

            # Parse with Pandas
            df = pd.read_csv(output_path)
            data = [
                {
                    'name': 'Evapotranspiration',
                    'mode': 'lines',
                    'x': df.iloc[:, 1].tolist(),
                    'y': df.iloc[:, 2].tolist(),
                    'line': {
                        'width': 2,
                        'color': 'red'
                    }
                },
            ]

            return f'Evapotranspiration at Catchment "{id}"', data, layout
'''

    def get_context(self, request, *args, **kwargs):
        """
        Create context for the Map Layout view, with an override for the map extents based on stream and weather gauges.

        Args:
            request (HttpRequest): The request.
            context (dict): The context dictionary.

        Returns:
            dict: modified context dictionary.
        """

        start_date_picker = DatePicker( 
            name='start-date',
            display_text='Start Date',
            autoclose=False,
            format='MM d, yyyy',
            start_date='1/1/2019',
            start_view='year',
            today_button=False, 
            initial='January 1, 2019'
        )
        end_date_picker = DatePicker( 
            name='end-date',
            display_text='End Date',
            start_date='6/11/2019',
            autoclose=False,
            format='MM d, yyyy',
            start_view='year',
            today_button=False, 
            initial='June 11, 2019'
        )

        # Call Super
        context = super().get_context(
            request,
            *args,
            **kwargs
        )
        context['start_date_picker'] = start_date_picker  
        context['end_date_picker'] = end_date_picker  
        #print(context)
        return context
        #return render(request, 'map_layout_tutorial/roset_view.html', context)