# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import csv
import math
import uuid
from pathlib import Path
import numpy as np


# 处理自己用qgis下载的影像瓦片
def xyz2LonLat():
    path = r'D:\dataSet\jiashouna\Yandex\18'
    # 1. 创建文件对象（指定文件名，模式，编码方式）a模式 为 下次写入在这次的下一行
    with open("file.csv", "a", encoding="utf-8", newline="") as f:
        f.truncate(0)
        # 2. 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_NONNUMERIC )
        # 3. 构建列表头
        name = ['Filename', 'Top_left_lat', "Top_left_lon", "Bottom_right_lat", "Bottom_right_long","Center_lat","Center_long","west", "south", "east", "north"]
        csv_writer.writerow(name)

        for filepath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                # filepathArr = filepath.split("\")
                pngPath = os.path.join(filepath, filename)
                png = pngPath.split("\\")
                for el in png:
                    length = len(png)
                    z = int(png[length-3])
                    x = int(png[length - 2])
                    y = int(png[length - 1].split(".")[0])
                Top_left_lat , Top_left_lon = num2deg(x,y,z)
                Bottom_right_lat, Bottom_right_long = num2deg(x+1, y+1, z)
                Center_lat, Center_long = num2deg(x + 0.5, y + 0.5, z)
                west, south, east, north = Top_left_lon,Bottom_right_lat,Bottom_right_long,Top_left_lat
                csv_writer.writerow([pngPath,Top_left_lat,Top_left_lon,Bottom_right_lat,Bottom_right_long,Center_lat,Center_long,west, south, east, north])

        # 5. 关闭文件
        print("写入数据完成")
        f.close()


# 处理dateset:University-Release
def createDataFrame():
    basePath = "F:/datasets/University-Release/train/"
    drone_path = r'F:\datasets\University-Release\train\drone'
    # 1. 创建文件对象（指定文件名，模式，编码方式）a模式 为 下次写入在这次的下一行
    with open("universityDataFrame.csv", "a", encoding="utf-8", newline="") as f:
        f.truncate(0)
        # 2. 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_NONNUMERIC )
        # 3. 构建列表头
        name = ['place_id','q_index',"q_img","ref_index","ref_img","ref_lon","ref_lat","panoid"]
        csv_writer.writerow(name)
        q_index = 0
        ref_index = 0
        currentQueryLastFolder = "0839"
        for filepath, dirnames, filenames in os.walk(drone_path):
            for filename in filenames:
                # filepathArr = filepath.split("\")
                qPath = os.path.join(filepath, filename)
                qPathArray = qPath.split("\\")
                qLastFolder = qPathArray[len(qPathArray)-2]

                qName = qPathArray[len(qPathArray)-1]
                q_img = "drone/"+qLastFolder+"/"+qName
                ref_img = "satellite/"+qLastFolder+"/"+qLastFolder+".jpg"
                if not Path(basePath+ref_img).exists():
                    raise FileNotFoundError(basePath+ref_img+' is not Found, please check it!')

                if qLastFolder != currentQueryLastFolder:
                    ref_index += 1
                    currentQueryLastFolder = qLastFolder

                q_index += 1
                q_panoid = uuid.uuid4().hex
                csv_writer.writerow([ref_index,q_index,q_img,ref_index,ref_img,0,0,q_panoid])




        # 5. 关闭文件
        print("写入数据完成")
        f.close()



def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (round(lat_deg,6), round(lon_deg,6))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    createDataFrame()
    # xyz2LonLat()

# z=18,h=120
#https://sandcastle.cesium.com/
# viewer.camera.setView({
#     destination : Cesium.Rectangle.fromDegrees(127.73391723632812,26.374646153883504,127.73529052734375,26.37587649032716)
# });

# viewer.camera.flyTo({
#     destination : Cesium.Cartesian3.fromDegrees(127.744904, 26.39556, 350.0)
# });