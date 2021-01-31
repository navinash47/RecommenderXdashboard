from math import radians, cos, sin, asin, sqrt
import numpy as np
import os
import sys
import json
from scipy.spatial import distance
import pickle
import json
import pandas as pd
def gen_json(hosp,ci):
    json_final=[]
    
    for index,row in hosp.iterrows():
        json_dic={}
        json_dic["error"]=False
        
        json_dic["phone"]=str(row["Phone_number"])
        json_dic["name"]=str(row["Name"])
        json_dic["Lat"]=str(row["Latitude"])
        json_dic["Lon"]=str(row["Longitude"])
        json_dic["nob"]=str(row["no_of_beds"])
        json_dic["noofhosp"]=str(len(hosp))
        json_dic["Rating"]=str(row["Rating"])
        json_dic["Department"]=str(row["Dept"])
        json_dic["ci"]=str(ci)
        json_final.append(json_dic)

    print(json_final) 
    return json.dumps(json_final)

def Sum(attr):
    Sum=0
    for i in attr:
        if(i!="nan"):
            Sum=Sum+float(i)
    return Sum

def normalize(attr):
    norm_attr=[]
    s=Sum(attr)
    for i in attr:
        if(i=="nan"):
            norm_attr.append(0)
        else:
            norm_attr.append(float(i)/s)
    return norm_attr

def cosine_similarity(calc,r):
    print("check")
    full=[]
    for index,row in calc.iterrows():
        full.append(1 - distance.cosine([row["norm_Rating"],row["norm_nob"],row["norm_Dis"]], r))
    return full

def euclid_similarity(calc,r):
    full=[]
    for index,row in calc.iterrows():
        full.append(distance.euclidean([row["norm_Rating"],row["norm_nob"],row["norm_Dis"]], r))
    return full
def check_dept(Hospital,cond_dept):
    flag=False
    print(str(Hospital["Dept"]))
    all_dept=str(Hospital["Dept"]).split(',')
    print(all_dept)
    for dept in cond_dept:
        if dept in str(Hospital["Dept"]).split(','): 
            flag=True
            break
    return flag
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def main_recomm( gender2,age,BT,PR,BOL,SBP,DBP,geo_lat,geo_lon):
    #get patients data as input

    #open model pickle
    pickle_in=open("model.pickle","rb")
    ml_model=pickle.load(pickle_in)
    
    if(gender2=='Male' or gender2=='male'):
        gender=1
    else:
        gender=0

    pred_args=[age,gender,BT,PR,BOL,SBP,DBP]
    pred_args_arr=np.array(pred_args)
    pred_args_arr=pred_args_arr.reshape(1,-1)

    #Writing predicted Critical Index value
    model_prediction=ml_model.predict(pred_args_arr)
    model_prediction=round(float(model_prediction),2)
    # return str(model_prediction)

    d=pd.read_csv("Hospitals.csv")
    # from app import     # #Fetch all hospitals


    # #finding hospitals in radius of 5 km 
    center_point = [{'lat': geo_lat, 'lng': geo_lat}]
    radius = 5.00 # in kilometer

    hosp=pd.DataFrame(columns=["Place_1","Place_2","Name","Latitude","Longitude","Rating","Vicinity","Place_id","Open_Status","Phone_number","Dept","no_of_beds"])
    dis=[]
    for index,row in d.iterrows():
        lat2=float(row["Latitude"])
        lon2=float(row["Longitude"])
        #assertion of point present within the radius
        a = haversine(float(geo_lon),float(geo_lat),float(lon2),float(lat2))
        if(a<=radius):
            hosp=hosp.append(row, ignore_index=True)
            dis.append(a)
    hosp["Dis"]=dis

    # # sort according to required departments 
    medium_ci=["public health","nan","general practice","general surgery"]
    high_ci=["cardiology","cardiothoracic surgery","cardiovascular surgery","intensive care medicine","specialty"]
    hosp1=pd.DataFrame(columns=["Place_1","Place_2","Name","Latitude","Longitude","Rating","Vicinity","Place_id","Open_Status","Phone_number","Dept","no_of_beds","Dis"])

    if float(model_prediction)<3:
        for index ,row in hosp.iterrows():         
            if check_dept(row,medium_ci):       
                hosp1=hosp1.append(row , ignore_index=True)
                    
    elif float(model_prediction)>=3:
        for index ,row in hosp.iterrows():
            if check_dept(row,high_ci):
                hosp1=hosp1.append(row , ignore_index=True)
    
    # #sort according to Rating
    hosp1=hosp1.sort_values('Rating', ascending=False).drop_duplicates('Name')
    hosp1=hosp1.sort_values('Rating', ascending=False).drop_duplicates('Place_id')
    
    rating=hosp1["Rating"]
    nob=hosp1["no_of_beds"]
    dis=hosp1["Dis"]

    rating=normalize(rating)
    nob=normalize(nob)
    dis=normalize(dis)

    hosp1["norm_Rating"]=rating
    hosp1["norm_nob"]=nob
    hosp1["norm_Dis"]=dis

    try:
        cal1=cosine_similarity(hosp1,[max(rating),max(nob),min(dis)])
        hosp2=hosp1
        hosp2["cosine"]=cal1
        hosp2=hosp2.sort_values('cosine', ascending=False)
    except:
        print("no Hospital")
        json_dic={}
        json_final=[]
        json_dic={"error":True,"message":"Cosine gone","len":str(len(hosp1))}
        json_final.append(json_dic)
        return json.dumps(json_final)

    # # print(hosp2)
    # try:
    #     cal2=euclid_similarity(hosp1,[max(rating),max(nob),min(dis)])
    #     hosp3=hosp1
    #     hosp3["euclid"]=cal2
    #     hosp3=hosp3.sort_values('euclid', ascending=False)
    # except:
    #     print("no Hospitals")
    #     json_dic={}
    #     json_final=[]
    #     json_dic={"error":True}
    #     json_final.append(json_dic)
    #     return json.dumps(json_final)

    
    # try:
    #     return gen_json(hosp2,model_prediction)
    # except:
    #     print("no Hospitals")
    #     json_dic={}
    #     json_final=[]
    #     json_dic={"error":True,"message":"Cosine hhgone","len":str(len(hosp2))+"-"+str(len(hosp1))}
    #     json_final.append(json_dic)
    #     return json.dumps(json_final)
    return gen_json(hosp2,model_prediction)


