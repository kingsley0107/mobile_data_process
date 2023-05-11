import pandas as pd
import geopandas as gpd
import transbigdata as tbd
from config.config import *


def boundary_to_grid(grid_size, BOUNDARY_PATH=BOUNDARY_PATH, OUTPUT_ROOT=OUTPUT_ROOT):
    """
        function to divide boundary into many grids, in the size of grid_size*grid_size

    Args:
        grid_size (_type_): indentify grid size(meters).
        BOUNDARY_PATH (_type_, optional): _description_. Defaults to BOUNDARY_PATH.
        OUTPUT_ROOT (_type_, optional): _description_. Defaults to OUTPUT_ROOT.
    """

    bd = gpd.read_file(BOUNDARY_PATH)
    grids, params = tbd.area_to_grid(bd, accuracy=grid_size)
    grids.to_file(OUTPUT_ROOT + "/grids/grids.shp")
    return grids, params


def detect_stay_move(
    params,
    stay_threshold,
    MOBILE_PATH=MOBILE_PATH,
    columns=columns_in_mobile,
    OUTPUT_ROOT=OUTPUT_ROOT,
):
    """
        function to detect home location

    Args:
        params (_type_): grids' information, used to match grids' ID ( LONCOL&LATCOL)
        stay_threshold (_type_): When the time interval between two adjacent data from the same user is greater than this threshold, the data is considered as 'stay
        MOBILE_PATH (_type_, optional): _description_. Defaults to MOBILE_PATH.
        columns (_type_, optional): Attention that the order of the columns. plz refer to config/config.py . Defaults to columns_in_mobile.
        OUTPUT_ROOT (_type_, optional): _description_. Defaults to OUTPUT_ROOT.

    Raises:
        ValueError: _description_

    Returns:
        stay: used to detect home & work location
    """

    if MOBILE_PATH.endswith(".xlsx"):
        mobile = pd.read_excel(MOBILE_PATH)
    elif MOBILE_PATH.endswith(".csv"):
        mobile = pd.read_csv(MOBILE_PATH, encoding="utf-8_sig")
    else:
        mobile = gpd.read_file(MOBILE_PATH)

    if mobile.empty:
        print("=================ERROR!==================")
        raise ValueError
    else:
        uuid, time, lng, lat = columns
        stay, move = tbd.mobile_stay_move(
            mobile, params, columns, activitytime=stay_threshold
        )
        stay = stay.sort_values([uuid, "stime"], ascending=[False, True])
        move = move.sort_values([uuid, "stime"], ascending=[False, True])
        stay.to_csv(OUTPUT_ROOT + "/activity/stay.csv", encoding="utf-8_sig")
        move.to_csv(OUTPUT_ROOT + "/activity/move.csv", encoding="utf-8_sig")
    return stay


def detect_home(staydata, daytime_start=8, daytime_end=20, columns=columns_in_mobile):
    uid, time, lng, lat = columns
    home = tbd.mobile_identify_home(
        staydata, [uid, "stime", "etime", "LONCOL", "LATCOL"]
    )
    home = home.reset_index(drop=True)
    home.to_csv(OUTPUT_ROOT + "/detected/matched_home.csv", encoding="utf-8_sig")
    return home


def detect_work(
    staydata, threshold=3, daytime_start=8, daytime_end=20, columns=columns_in_mobile
):
    """
        function to detect work location

    Args:
        staydata (_type_): _description_
        threshold (int, optional): _description_. Defaults to 3.
        daytime_start (int, optional): _description_. Defaults to 8.
        daytime_end (int, optional): _description_. Defaults to 20.
        columns (_type_, optional): _description_. Defaults to columns_in_mobile.

    Returns:
        _type_: _description_
    """
    uid, time, lng, lat = columns
    work_location = tbd.mobile_identify_work(
        staydata,
        [uid, "stime", "etime", "LONCOL", "LATCOL"],
        minhour=threshold,
        start_hour=daytime_start,
        end_hour=daytime_end,
    )
    work_location = work_location.reset_index(drop=True)
    work_location.to_csv(
        OUTPUT_ROOT + "/detected/matched_work_location.csv", encoding="utf-8_sig"
    )
    return work_location


def schedule():
    """
    function to schedule the tasks
    """
    grids, params = boundary_to_grid(grid_size=GRID_SIZE)
    stay = detect_stay_move(params=params, stay_threshold=STAY_THRESHOLD)
    detect_home(staydata=stay, daytime_start=DAYTIME_START, daytime_end=DAYTIME_END)
    detect_work(
        staydata=stay,
        threshold=WORK_THRESHOLD,
        daytime_start=DAYTIME_START,
        daytime_end=DAYTIME_END,
    )
