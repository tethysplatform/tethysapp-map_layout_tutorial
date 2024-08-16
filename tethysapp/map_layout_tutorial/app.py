from tethys_sdk.base import TethysAppBase


class App(TethysAppBase):
    """
    Tethys app class for Map Layout Tutorial.
    """

    name = 'Map Layout Tutorial'
    description = ''
    package = 'map_layout_tutorial'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/noaa_digital_logo-2022.png'
    root_url = 'map-layout-tutorial'
    color = '#003087'
    tags = ''
    enable_feedback = False
    feedback_emails = []