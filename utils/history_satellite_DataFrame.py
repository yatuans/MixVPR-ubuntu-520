# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import csv
import math
import uuid
from pathlib import Path
import numpy as np
import glob

# 制作VAL dateset:history_satellite
def createHistorySatelliteDataFrame():
    #cities = ["jiashouna","mianbei","ukrian","ukrian-part","xiangang","xinzu"]
    cities = ["ukrian-part"]
    basePath = "F:/datasets/yts_history_satellite_from_esri/"
    base_path = r'F:\datasets\yts_history_satellite_from_esri'
    savePath = "F:/datasets/yts_history_satellite_from_esri/Dataframes/"
    for city in cities:
        # 1. 创建文件对象（指定文件名，模式，编码方式）a模式 为 下次写入在这次的下一行
        csv_path = savePath + city + ".csv"
        ref_path = base_path + "\\" + city + "\\ref\\"
        query_path = basePath + city + "/query/"
        ref_list = os.listdir(ref_path)
        # 打印所有文件名
        for ref_date in ref_list:
            print(ref_date)
            ref_path = ref_path + ref_date + "\\瓦片_谷歌\\17\\"

        dbImages = []
        qImages = []
        qIdx = []
        pIdx = []
        with open(csv_path, "a", encoding="utf-8", newline="") as f:
            f.truncate(0)
            # 2. 基于文件对象构建 csv写入对象
            csv_writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            # 3. 构建列表头
            name = ['place_id', 'q_index', "q_img", "ref_index", "ref_img", "ref_lon", "ref_lat", "panoid"]
            csv_writer.writerow(name)
            q_index = 0
            ref_index = 0

            for filepath, dirnames, filenames in os.walk(ref_path):
                for filename in filenames:
                    # print(filename)
                    # filepathArr = filepath.split("\")
                    rPath = os.path.join(filepath, filename)
                    rPathArray = rPath.split("\\")
                    # print(rPathArray)
                    rLastFolder = rPathArray[len(rPathArray) - 2]
                    ref_date = rPathArray[len(rPathArray) - 5]
                    rName = rPathArray[len(rPathArray) - 1]
                    z = int(rPathArray[len(rPathArray) - 3])
                    x = int(rPathArray[len(rPathArray) - 2])
                    y = int(rPathArray[len(rPathArray) - 1].split(".")[0])
                    ref_lat, ref_lon = num2deg(x + 0.5, y + 0.5, z)

                    ref_img = city + "/ref/" + ref_date + "/瓦片_谷歌/17/" + rLastFolder + "/" + rName

                    query_list = os.listdir(query_path)
                    # 打印所有文件名
                    # print(len(query_list))
                    for index, query_date in enumerate(query_list):
                        # print(query_date)
                        q_img = city + "/query/" + query_date + "/瓦片_谷歌/17/" + rLastFolder + "/" + rName
                        # print(query_path + query_date+"/瓦片_谷歌/17/"+rLastFolder+"/"+rName)
                        checkPath = query_path + query_date + "/瓦片_谷歌/17/" + rLastFolder + "/" + rName
                        if not Path(checkPath).exists():
                            print(checkPath + ' is not Found, please check it!')
                            continue
                            # raise FileNotFoundError(checkPath + ' is not Found, please check it!')

                        qImages.append(q_img)
                        qIdx.append(q_index)
                        q_index += 1
                        q_panoid = uuid.uuid4().hex
                        pIdx.append(ref_index)
                        csv_writer.writerow([ref_index, q_index, q_img, ref_index, ref_img, ref_lon, ref_lat, q_panoid])

                    dbImages.append(ref_img)
                    ref_index += 1

            # 5. 关闭文件
            print("写入数据完成")
            f.close()

            # print(dbImages)
            # print(pIdx)
            # print(f'len of dbImages:{len(dbImages)}')
            # print(f'len of pIdx:{len(pIdx)}')
            # print(f'len of qImages:{len(qImages)}')
            # print(f'len of qIdx:{len(qIdx)}')


            # hard code
            np.save(savePath + city + '_dbImages.npy', dbImages)
            np.save(savePath + city + '_qImages.npy', qImages)
            np.save(savePath + city + '_qIdx.npy', qIdx)
            np.save(savePath + city + '_pIdx.npy', pIdx)

            # a = np.load(basePath+city+"/"+city+'_dbImages.npy', allow_pickle=True)
            # print(a)


def createVpairDataFrame():
    print("createVpairDataFrame")
    basePath = "F:/datasets/vpair_sample/"
    base_path = r'F:\datasets\vpair_sample'
    savePath = "F:/datasets/vpair_sample/Dataframes/"
    cities=["vpair"]

    for city in cities:
        # 1. 创建文件对象（指定文件名，模式，编码方式）a模式 为 下次写入在这次的下一行
        csv_path = savePath + city + ".csv"
        ref_path = base_path + "\\reference_views\\"
        query_path = basePath + "/queries/"
        dbImages = []
        qImages = []
        with open(csv_path, "a", encoding="utf-8", newline="") as f:
            f.truncate(0)
            # 2. 基于文件对象构建 csv写入对象
            csv_writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            # 3. 构建列表头
            name = ['place_id', 'q_index', "q_img", "ref_index", "ref_img", "ref_lon", "ref_lat", "panoid"]
            csv_writer.writerow(name)
            q_index = 0
            ref_index = 0
            qGlobs = glob.glob(query_path + '/*.png', recursive=True)
            dGlobs = glob.glob(ref_path + '/*.png', recursive=True)
            length = len(qGlobs)
            qIdx = [num for num in range(length)]
            pIdx = [num for num in range(length)]
            for fPath in qGlobs:
                fPathArray = fPath.split("\\")
                ref_img = "reference_views/" + fPathArray[len(fPathArray) - 1]
                dbImages.append(ref_img)
                q_img = "queries/" + fPathArray[len(fPathArray) - 1]
                qImages.append(q_img)
                q_panoid = uuid.uuid4().hex
                csv_writer.writerow([ref_index, q_index, q_img, ref_index, ref_img, 0, 0, q_panoid])
                ref_index += 1
                q_index += 1


            # 5. 关闭文件
            print("写入数据完成")
            f.close()
            print(qImages)
            print(qIdx)
            # print(f'len of dbImages:{len(dbImages)}')
            # print(f'len of pIdx:{len(pIdx)}')
            # print(f'len of qImages:{len(qImages)}')
            # print(f'len of qIdx:{len(qIdx)}')
            # hard code
            np.save(savePath + city + '_dbImages.npy', dbImages)
            np.save(savePath + city + '_qImages.npy', qImages)
            np.save(savePath + city + '_qIdx.npy', qIdx)
            np.save(savePath + city + '_pIdx.npy', pIdx)



def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (round(lat_deg,7), round(lon_deg,7))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    createHistorySatelliteDataFrame()
    # createVpairDataFrame()
