import xlwt
import xlrd
import requests
import urllib
import math
import re
import json
import time
#采用V2路径规划
#输入数据：为point_pair.xlsx数据，输入数据第一列 序号、第二列 经度、 第三列 纬度
#需要自行修改出行模式mode
#需要修改AK值

#输出数据为在输入数据基础上，添加了对应点到终点的时长xls数据（异常值为-9999）

#终点坐标代码中固定值



# 通过request获取返回时间

def get_time(coordinate, mode):
    # http://api.map.baidu.com/direction/v2/driving?origin=40.01116,116.339303&destination=39.936404,116.452562&ak=您的AK
    # add your AK in the next line
    api_addr = "http://api.map.baidu.com/direction/v2/" + mode + "?origin=" + coordinate + "&destination=34.437629,108.757279&output=json&coord_type=wgs84&ak=PLEASE ENTER YOUR REAL AK NUMBER"

    req = requests.get(api_addr)
    content = req.content
    sjson = json.loads(content)
    if "result" in sjson:
        if sjson["status"] == 0:
            if mode == "transit":  # 公交
                if sjson["result"].has_key("routes"):
                    if sjson["result"]["routes"][0].has_key("scheme"):
                        time = sjson["result"]["routes"][0]["scheme"][0]["duration"]
                    else:
                        time = sjson["result"]["routes"][0]["duration"]
                else:
                    time = 0
            else:  # 其他出行模式
                if "routes" in sjson["result"]:
                    # if sjson["result"].has_key("routes"): #python 3 以后不用这种写法
                    if sjson["result"]["routes"] == None:
                        time = 0
                    else:
                        time = sjson["result"]["routes"][0]["duration"]
                else:
                    time = 0
        else:
            time = 0
    else:
        time = 0
    # print(coordinate, time)
    return time

def run():
    # mode是模式driving（驾车）、walking（步行）、transit（公交）、riding（骑行）
    mode = "driving"

    # data 是输入的表格
    pathin = r"point_pair_filename.xlsx"
    data = xlrd.open_workbook(pathin)
    rtable = data.sheets()[0]
    nrows = rtable.nrows

    workbook = xlwt.Workbook()
    # 新建输出表格
    wtable = workbook.add_sheet('driving_zxd_p', cell_overwrite_ok=True)
    row = 0

    for i in range(nrows):
        # 输入数据第一列 序号、第二列 经度、 第三列 纬度
        s1 = str(rtable.row_values(i)[2]) + "," + str(rtable.row_values(i)[1])
        print(i)
        try:
            time = get_time(s1, mode)
            print(str(time)+"s")
            wtable.write(row, 0, rtable.row_values(i)[0])
            wtable.write(row, 1, rtable.row_values(i)[1])
            wtable.write(row, 2, rtable.row_values(i)[2])
            wtable.write(row, 3, time)  # 时间
            row = row + 1
        except OSError:
            time = -9999 #异常值
            print(str(time)+"s")
            wtable.write(row, 0, rtable.row_values(i)[0])
            wtable.write(row, 1, rtable.row_values(i)[1])
            wtable.write(row, 2, rtable.row_values(i)[2])
            wtable.write(row, 3, time)  # 时间
            row = row + 1
        continue

    # 保存输出表格
    pathout = r"time_second_filename.xls"
    workbook.save(pathout)


if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    run()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))