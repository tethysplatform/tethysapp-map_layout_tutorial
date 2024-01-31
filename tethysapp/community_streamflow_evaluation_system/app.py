from tethys_sdk.base import TethysAppBase
from tethys_sdk.app_settings import CustomSetting, SecretCustomSetting

class CSES(TethysAppBase):
    """
    Tethys app class for Map Layout Tutorial.
    """

    name = 'Community Streamflow Evaluation System (CSES)'
    package = 'community_streamflow_evaluation_system'
    index = 'home'
    icon = f'{package}/images/CSESoverviewImage.JPG' 
    root_url = 'community-streamflow-evaluation-system' 
    color = '#003087'
    description = (
        '"A tethys app that lets the user to visualize and query modeled streamflow'
    )
    tags = '"Hydrology", "WMO", "BYU"'
    enable_feedback = False
    feedback_emails = []
    controller_modules = ["controllers", "State_Controller", "Reach_Controller", "HUC_Controller"]
 
    def custom_settings(self):
        """
        Example custom_settings method.
        """
        custom_settings = (
            CustomSetting(
                name='Access_key_ID',
                type=CustomSetting.TYPE_STRING, 
                description='AWS bucket S3 Access Key',
                required=True
            ),
            SecretCustomSetting(
                name='Secret_access_key',
                description='AWS bucket S3 Secret access Key',
                required=True
            ),

        )

        return custom_settings