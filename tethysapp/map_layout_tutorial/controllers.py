from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import App

@controller(name="home", app_workspace=True)
class MapLayoutTutorialMap(MapLayout):
    app = App
    base_template = f'{App.package}/base.html'
    map_title = 'Map Layout Tutorial'
    map_subtitle = 'NOAA-OWP NextGen Model Outputs'