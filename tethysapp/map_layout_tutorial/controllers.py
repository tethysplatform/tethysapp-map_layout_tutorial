import json
from pathlib import Path
import pandas as pd

from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import MapLayoutTutorial as app

#functions to load AWS data
import boto3
import os

#Date picker
from tethys_sdk.gizmos import DatePicker
from django.shortcuts import render
from tethys_sdk.gizmos import DatePicker
import datetime
from django.http import JsonResponse

MODEL_OUTPUT_FOLDER_NAME = 'sample_nextgen_data'
INIT_DATE='8/22/2022'
END_DATE='8/23/2022'
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

    def update_dates(self, request, *args, **kwargs):
        """
        Custom REST method for updating data form Map Layout view.
        """
        parms = request.GET
        # breakpoint()
        print(parms)
        ...
        return JsonResponse({'success': True})


    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs):
        """
        Add layers to the MapLayout and create associated layer group objects.
        """
        # data_test = request.GET.get('other')
        # print(data_test)
        # Load GeoJSON from files
        config_directory = Path(app_workspace.path) / MODEL_OUTPUT_FOLDER_NAME / 'config'
        
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

        # flowpaths
        flowpaths_path = config_directory / 'flowpaths_4326.geojson'
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

        # USGS stations
        staions_path = config_directory / 'StreamStats_AL_4326.geojson'
        with open(staions_path) as ff:
            stations_geojson = json.loads(ff.read())

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
                    nexus_layer,
                    catchments_layer,
                    flowpaths_layer
                    
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
        # breakpoint()
        print(request)

        #class function to load using AWS data
        #load access key
        home = Path(app_workspace.path) #"./workspaces/app_workspace"
        keypath = "AWSaccessKeys.csv"
        access = pd.read_csv(f"{home}/{keypath}")

        #start session
        session = boto3.Session(
            aws_access_key_id=access['Access key ID'][0],
            aws_secret_access_key=access['Secret access key'][0],
        )
        self.s3 = session.resource('s3')
        #AWS bucket information
        bucket_name = 'streamflow-app-data'
        #s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
        self.bucket = self.s3.Bucket(bucket_name)

        #output directory for AWS
        output_directory = 'MapLayout/Nexus'
        #output_directory = Path(app_workspace.path) / MODEL_OUTPUT_FOLDER_NAME / 'outputs' # change this to S3, model output folder could be the model name in S3
        print(output_directory)
        

        # Get the feature id
        id = feature_props.get('id') 
        '''need to create our own geojson files, likely for usgs sites and nhd reaches 
        1. start with points (usgs locations) - reach class first, then huc class if time
        2. add nhdplus reaches for colocated usgs sites
        3. add all nhdplus reaches (blue lines) for all available nhdplus streams in the HUC 
        4. Add catchment extend, depending on input huc?

        '''

        # Nexus
        if layer_name == 'nexus':
            layout = {
                'yaxis': {
                    'title': 'Streamflow (cfs)'
                }
            }

            output_path = f'{output_directory}/{id}_output.csv' 
         

            #if not output_path.exists():
             #   print(f'WARNING: no such file {output_path}')
              #  return f'No Data Found for Nexus "{id}"', [], layout

            # Parse with Pandas
            #df = pd.read_csv(output_path)# this file format is the same as ours!
            #Using AWS
            obj = self.bucket.Object(output_path)
            body = obj.get()['Body']
            df = pd.read_csv(body)
            df.pop('0')

           

            time_col = df.iloc[:, 0] # date, adjust per Data source
            #streamflow_cms_col = df.iloc[:, 2] # streamflow, adjust per Data source, Tethys demo
            streamflow_cms_col = df.iloc[:, 1] # streamflow, adjust per Data source, AWS demo
            streamflow_cfs_col = streamflow_cms_col * 35.314  # Convert to cfs
            streamflow_cfs_col2 = streamflow_cfs_col*1.2
            data = [
                {
                    'name': 'Streamflow',
                    'mode': 'lines',
                    'x': time_col.tolist(),
                    'y': streamflow_cfs_col.tolist(),
                    'line': {
                        'width': 2,
                        'color': 'blue'
                    }
                },
                {
                    'name': 'Streamflow scaled',
                    'mode': 'lines',
                    'x': time_col.tolist(),
                    'y': streamflow_cfs_col2.tolist(),
                    'line': {
                        'width': 2,
                        'color': 'red'
                    }
                },
            ]


            return f'Streamflow at Nexus "{id}"', data, layout

        # Catchments
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
        
        # flowpaths
        if layer_name == 'flowpaths':
            layout = {
                'yaxis': {
                    'title': 'Streamflow (cfs)'
                }
            }

            output_path = output_directory / f'{id}_output.csv' # this file format is the same as ours!
            if not output_path.exists():
                print(f'WARNING: no such file {output_path}')
                return f'No Data Found for flowpath "{id}"', [], layout

            # Parse with Pandas
            df = pd.read_csv(output_path)# this file format is the same as ours!
            time_col = df.iloc[:, 1] # we could also subset for date/time here too
            streamflow_cms_col = df.iloc[:, 2] # we could also subset for date/time here too
            streamflow_cfs_col = streamflow_cms_col * 35.314  # Convert to cfs
            streamflow_cfs_col2 = streamflow_cfs_col*1.2
            data = [
                {
                    'name': 'Streamflow',
                    'mode': 'lines',
                    'x': time_col.tolist(),
                    'y': streamflow_cfs_col.tolist(),
                    'line': {
                        'width': 2,
                        'color': 'blue'
                    }
                },
                {
                    'name': 'Streamflow scaled',
                    'mode': 'lines',
                    'x': time_col.tolist(),
                    'y': streamflow_cfs_col2.tolist(),
                    'line': {
                        'width': 2,
                        'color': 'red'
                    }
                },
            ]


            return f'Streamflow in flowpath "{id}"', data, layout


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
            start_date='8/22/2022',
            start_view='month',
            today_button=False, 
            initial='August 22, 2022'
        )
        end_date_picker = DatePicker( 
            name='end-date',
            display_text='End Date',
            start_date='8/23/2022',
            autoclose=False,
            format='MM d, yyyy',
            start_view='month',
            today_button=False, 
            initial='September 5, 2022'
        )

        # Call Super
        context = super().get_context(
            request,
            *args,
            **kwargs
        )
        context['start_date_picker'] = start_date_picker  
        context['end_date_picker'] = end_date_picker  

        return context
        return render(request, 'map_layout_tutorial/roset_view.html', context)