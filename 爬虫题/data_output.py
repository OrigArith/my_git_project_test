import json
import pandas as pd
import datetime

def read_comments():
    with open('comments.json', 'r', encoding='utf-8') as f:
        comments = json.load(f)
    return comments

output_list = []

comments = read_comments()
print(len(comments["data"]["comments"]))

for item in comments["data"]["comments"]:
    user_info = {}
    for key, value in item["user"].items():
        user_info["user-"+key] = value

    item.pop("beReplied")
    item.pop("user")
    item.pop("showFloorComment")
    item.pop("decoration")
    item.pop("tag")
    
    extInfo_endpoint_info = {}
    for key, value in item["extInfo"]["endpoint"].items():
        extInfo_endpoint_info["extInfo-endpoint-"+key] = value
        
    ipLocation_info = {}
    for key, value in item["ipLocation"].items():
        ipLocation_info["ipLocation-"+key] = value
        
    item.pop("extInfo")
    item.pop("ipLocation")
    
    item.update(user_info)
    item.update(extInfo_endpoint_info)
    item.update(ipLocation_info)
    
    output_list.append(item)
# 将时间戳转换为时间 

for out_item in output_list: 
    com_time = out_item["time"]
    time_stamp = datetime.datetime.fromtimestamp(com_time/1000)
    time_stamp_str = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
    out_item["time"] = time_stamp_str
    


df = pd.DataFrame(output_list)
df.to_csv("comments.csv",index=False,encoding='utf-8')