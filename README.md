ENGLISH [中文版](./zh-cn.md)
# MOBILE_DATA_PROCESS
This project is a user mobile data analysis tool based on transbigdata (Python). It is used to process and analyze mobile signaling data, distinguishing and extracting individual user activities and stay points to detect their residential and work locations. It can be used for research, learning, and analysis in the field of urban science.

## Features
- Grid partitioning of the study area
- Detection and differentiation of user stay trajectory data and mobile trajectory data
- Identification of user residential and work locations

## Usage Instructions
-   Make sure you have installed all the required Python libraries:
    -   pandas
    -   geopandas
    -   transbigdata
-   Configure the config/config.py file:
    -   MOBILE_PATH: Input the path to your signaling data set, which can be a .csv or .xlsx file.
    -   BOUNDARY_PATH: Input the path to the boundary data of the city's administrative areas, which can be a .shp or .geojson file.
    -   columns_in_mobile: Corresponding to the ['User ID', 'Timestamp', 'Longitude', 'Latitude'] fields in your signaling data.
    -   GRID_SIZE: Grid size (m) for partitioning the city.
    -   DAYTIME_START: Start time of daytime used to divide the time boundary for detecting residential and work locations.
    -   DAYTIME_END: End time of daytime.
    -   STAY_THRESHOLD: Threshold for mobile signaling trajectory point movement-stay determination.
    -   WORK_THRESHOLD: Time threshold for detecting work locations.
-   Once the configuration is completed, run main.py directly.

## What Results Will You Get?
-   grids.shp: Vector file of the grid partitioning, stored in the results/grids folder. It has LONCOL and LATCOL indicating the grid identifiers.
-   stay.csv: Individual user stay data, stored in the results/activity folder. Each row records the spatial-temporal information of a specific user during a certain period of time in a stationary state. The time includes the start time and end time, and the spatial information corresponds to the LONCOL and LATCOL identifiers, which are one-to-one with grids.shp.
-   move.csv: Individual user activity data, similar to stay.csv, stored in the results/activity folder.
-   matched_home.csv: Detected residential location results for individual users, representing the location where the user stayed the longest during the nighttime period in the signaling data. Stored in the results/detected folder.
-   matched_work_location.csv: Detected work location results for individual users, representing the location where the user stayed the longest during the daytime period in the signaling data, with a threshold greater than a certain value (configured in config.py).

## Algorithm Principle
- Trip chain construction + time window division. The principle of detecting residential locations is to extract the spatial location where the user stayed the longest during the 20:00 to 8:00 time period. The principle for detecting work locations is similar.
- More information is mentioned in references
![principal](./pics/prin.png)

## Dependency Repository
- transbigdata(https://github.com/ni1o1/transbigdata)

## References:
- 曹劲舟,涂伟,李清泉等.基于大规模手机定位数据的群体活动时空特征分析[J].地球信息科学学报,2017,19(04):467-474.
- Qing Yu, & Jian Yuan. (2022). TransBigData: A Python package for transportation spatio-temporal big data processing, analysis and visualization (v0.3.7). Zenodo. https://doi.org/10.5281/zenodo.6236507