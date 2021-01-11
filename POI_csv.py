#-*-coding:UTF-8-*-

import json
import csv
import sys
import requests #导入requests库，这是一个第三方库，把网页上的内容爬下来用的
ty=sys.getfilesystemencoding()
#print(ty)#这个可以获取文件系统的编码形式
import time

lat_1=10 #纬度范围lat1-lat2 lower-left point
lon_1=120 #经度范围lon1-lon2 lower-left point
lat_2=15   #upper-right point
lon_2=125   #upper-right point

las=1 #给las一个值1

ak= 'PLEASE ENTER YOUR REAL AK NUMBER' #add your real AK here!!!attention
#f=open('park.txt','a')
out=open('outname.csv','a',newline='')
csv_write=csv.writer(out,dialect='excel')
print (time.time())
print ('being')
urls=[] # 声明一个数组列表
lat_count=int((lat_2-lat_1)/las+0.1)
lon_count=int((lon_2-lon_1)/las+0.1)
for lat_c in range(0,lat_count):
    lat_b1=lat_1+las*lat_c
    for lon_c in range(0,lon_count):
        lon_b1=lon_1+las*lon_c
        for i in range(0,20):
            page_num=str(i)
            # you can add the name after query=
            url='http://api.map.baidu.com/place/v2/search?query=医院&' \
                ' bounds='+str(lat_b1)+','+str(lon_b1)+','+str(lat_b1+las)+','+str(lon_b1+las)+'&page_size=20&page_num='+str(page_num)+'&output=json&ak='+ak
            urls.append(url)



print ('url列表读取完成')
for url in urls:
    time.sleep(10)  #为了防止并发量报警，设置了一个10秒的休眠。
    print(url)
    html=requests.get(url)#获取网页信息
    data=html.json() #获取网页信息的json格式数据
    print(data)
    for item in data['results']:
        jname1 = item['province']
        jname2 = item['city']
        jname3 = item['area']
        jname4 = item['name']
        jname=jname1+jname2+jname3+jname4
        j_uid=item['uid']
        jstreet_id=item.get('street_id')
        jlat=item['location']['lat']

        jlon=item['location']['lng']

        jaddress=item['address']

        jphone=item.get('telephone')

        j_str=(jname,j_uid,jstreet_id,str(jlat),str(jlon),jaddress,jphone)

        print(j_str)

        csv_write.writerow(j_str)
        print("write over")
        #f.write(j_str)

    print (time.time())

#f.close()

print ('bingo')
