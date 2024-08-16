import json
from pathlib import Path
from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import App

@controller(name="home", app_workspace=True)
class MapLayoutTutorialMap(MapLayout):
    app = App
    base_template = f'{App.package}/base.html'
    map_title = 'Map Layout Tutorial'
    map_subtitle = 'NOAA-OWP NextGen Model Outputs'
    default_map_extent = [-87.83371926334216, 33.73443611122197, -86.20833410475134, 34.456557011634175]
    max_zoom = 14
    min_zoom = 9

    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs):
        """
        Add layers to the MapLayout and create associated layer group objects.
        """
        # Load GeoJSON from files
        config_directory = Path(app_workspace.path) / 'sample_nextgen_data' / 'config'

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

        # Create layer groups
        layer_groups = [
            self.build_layer_group(
                id='ngen-features',
                display_name='NGen Features',
                layer_control='checkbox',  # 'checkbox' or 'radio'
                layers=[
                    nexus_layer,
                    catchments_layer,
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
        }