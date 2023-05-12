from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import MapLayoutTutorial as app


@controller(name="home", app_workspace=True)
class MapLayoutTutorialMap(MapLayout):
    app = app
    base_template = 'map_layout_tutorial/base.html'
    map_title = 'Map Layout Tutorial'
    map_subtitle = 'NOAA-OWP NextGen Model Outputs'
