
![Github_top](https://user-images.githubusercontent.com/33735397/206313977-e67ba652-3340-4a1b-b1d1-141d8d5001f2.PNG)

# Community Streamflow Evaluation System (CSES)

![GitHub](https://img.shields.io/github/license/whitelightning450/Community-Streamflow-Evaluation-System?logo=GitHub&style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/whitelightning450/Community-Streamflow-Evaluation-System?style=plastic)
![GitHub repo size](https://img.shields.io/github/repo-size/whitelightning450/Community-Streamflow-Evaluation-System?logo=Github&style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/whitelightning450/Community-Streamflow-Evaluation-System?style=plastic)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/whitelightning450/Community-Streamflow-Evaluation-System?style=plastic)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/whitelightning450/Community-Streamflow-Evaluation-System?style=plastic)
![GitHub branch checks state](https://img.shields.io/github/checks-status/whitelightning450/Community-Streamflow-Evaluation-System/main?style=plastic)
![GitHub issues](https://img.shields.io/github/issues/whitelightning450/Community-Streamflow-Evaluation-System?style=plastic)
![GitHub milestones](https://img.shields.io/github/milestones/closed/whitelightning450/Community-Streamflow-Evaluation-System?style=plastic)
![GitHub milestones](https://img.shields.io/github/milestones/open/whitelightning450/Community-Streamflow-Evaluation-System?style=plastic)
![GitHub milestones](https://img.shields.io/github/milestones/open/whitelightning450/Community-Streamflow-Evaluation-System?style=plastic)

A Novel Community Streamflow Evaluation System (CSES) to evaluate hydrological model performance using a standardized NHDPlus data model.
CSES evaluates modeled streamflow to a repository of over 5,000 in situ USGS monitoring sites, with interactive visualizations supporting an in-depth analysis.

## Application Overview
National-scale streamflow modeling remains a modern challenge, as changes in the underlying hydrology from land use and land cover (LULC) change, anthropogentic streamflow modification, and general process components (reach length, hydrogeophysical processes, precipitation, temperature, etc) greatly influence  hydrological modeling.
In a changing climate, there is a need to anticipate flood intensity, impacts of groundwater depletion on streamflow, western mountain low-flow events, eastern rain-on-snow events, storm-induced flooding, and other severe environmental problems that challenge the management of water resources.
Given the National Water Model (NWM) bridges the gap between the spatially coarse USGS streamflow observations by providing a near-continuous 2.7 million reach predictions of streamflow using the standardized NHDPlus framework, there lies the potential to improve upon the capabilities of the model by characterizing predictive performance across the heterogeneity of processes and land covers present at the national scale. 
The python-based Community-Streamflow-Evaluation-System package provides a foundation to evaluate national hydrography dataset (nhd) based model outputs with colocated USGS/NWIS streamflow monitoring stations (parameter: 060) without the need to download in-situ or NWM v2.1 data (NWM v3.0 coming soon!). 
The package contains three key methods for evaluation: state-based LULC, HUC level analysis, and USGS station-based analysis.
Below is a description of each method and application.
Designed to assess NWM version 2.1 retrospective performance, by using the exemplified data model the tool can evaluate other model predictions, with the motivation to improve regionally dominant hydrological modeling skill.
By using Community-Streamflow-Evaluation-System, researchers can identify locations where a model may benefit from further training/calibration/parameterization or a need for new model processes/features (e.g., integration of reservoir release operations) to ultimately create new post-processing methods and/or hydrological modeling formulations to improve streamflow prediction capabilities with respect to modeling needs (e.g., stormflow, supply, emergency management, flooding, etc).   

### Data Access
Community-Streamflow-Evaluation-System leverages USGS/NWIS observations from 1980-2020 and colocated and while all data is publically available through the respective agencies, we found the download time to be preventative for a timely model evaluation. 
The Alabama Water Institute at the University of Alabama hosts NWM v2.1 retrospective for all colocated USGS monitoring stations at a daily temporal resolution and provides the data free of charge via access to Amazon AWS S3 cloud storage.
Community-Streamflow-Evaluation-System can quickly access observed and predicted data supporting a fast and repeatable tool for evaluating modeled streamflow performance.
