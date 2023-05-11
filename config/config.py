import os

# =============配置区==================

# 数据路径

# 输入你自己的信令数据集(xlsx也可以)
MOBILE_PATH = r"./dir/raw.csv"
# 城市行政区域边界数据(shp也可以)
BOUNDARY_PATH = r"./dir/shenzhen.geojson"


# 请将你的信令数据中代表以下数据的字段名称依次填入columns_in_mobile：['用户唯一标识','数据发生时间','经度','纬度']
# 为了避免异常错误，字段名尽量用英文
columns_in_mobile = ["uuid", "time", "wgs_lng", "wgs_lat"]

# GRID_SIZE:网格大小(m)（将城市进行网格划分，后续研究基于网格进行计算）
GRID_SIZE = 500

# DAYTIME_START：白天开始时间（默认8点钟），用于区分开检测居住地与工作地点的时间划分界限。
DAYTIME_START = 8

# DAYTIME_END: 白天结束时间(默认晚上8点)
DAYTIME_END = 20

# STAY_THRESHOLD：手机信令轨迹点移动-静止判断阈值。若相邻两条数据时间差大于STAY_THRESHOLD秒，则认为这段时间该用户为静止状态，小于则认为处于活动/移动状态
STAY_THRESHOLD = 1800

# WORK_THRESHOLD：工作地点检测的时间阈值。白天时间内至少停留满WORK_THRESHOLD小时的地方才能被认为是工作地点，小于该阈值则认为不是工作地点。
WORK_THRESHOLD = 3


# =============配置区==================


# ==========非配置区=================
OUTPUT_ROOT = r"./results"
if not os.path.isdir(OUTPUT_ROOT):
    os.makedirs(OUTPUT_ROOT)
    os.makedirs(OUTPUT_ROOT + "/activity")
    os.makedirs(OUTPUT_ROOT + "/grids")
    os.makedirs(OUTPUT_ROOT + "/detected")
else:
    print(f"{OUTPUT_ROOT} existed.")
# ==========非配置区=================
