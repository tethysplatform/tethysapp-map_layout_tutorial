from tethys_sdk.base import TethysAppBase


class MapLayoutTutorial(TethysAppBase):
    """
    Tethys app class for Map Layout Tutorial.
    """

    name = 'Map Layout Tutorial'
    description = ''
    package = 'map_layout_tutorial'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.gif'
    root_url = 'map-layout-tutorial'
    color = '#f39c12'
    tags = ''
    enable_feedback = False
    feedback_emails = []