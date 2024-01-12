from tethys_sdk.base import TethysAppBase


class MapLayoutTutorial(TethysAppBase):
    """
    Tethys app class for Map Layout Tutorial.
    """

    name = 'Community Streamflow Evaluation System (CSES)'
    package = 'map_layout_tutorial'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/CSES_eval.jpg'
    root_url = 'map-layout-tutorial'
    color = '#003087'
 
  