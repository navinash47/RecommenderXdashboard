from app import app
from flask import request,send_from_directory
from app import functions_for_dashboard as ffd
from app import recommender_plugin as rp
@app.route("/",methods=["POST","GET"])
def Recomm():
    if request.method =='POST':
        gender=request.form['Gender']
        age=float(request.form['Age'])
        BT=float(request.form['BT'])
        PR=float(request.form['PR'])
        BOL=float(request.form['BOL'])
        SBP=float(request.form['SBP'])
        DBP=float(request.form['DBP'])
        lat=float(request.form['Latitude'])
        lon=float(request.form['Longitude'])
        return rp.main_recomm(gender,age,BT,PR,BOL,SBP,DBP,lat,lon)
    return "error"
        
    # pass
@app.route("/getcsv",methods=['GET','POST'])
def gen_csv():
    if request.method =='POST':
        name=request.form['name']
        phone_no=request.form['phone_no']
        from_date=request.form['from_date']
        to_date=request.form['to_date']
        file_name=phone_no+"_"+from_date+"_"+to_date+".csv"
        # ffd.plugin_csv(name,phone_no,from_date,to_date,file_name)
        return ffd.plugin_csv(name,phone_no,from_date,to_date,file_name)
    return "error"
    
@app.route("/getcsv/<path:filename>",methods=['GET','POST'])
def download_file(filename):
    return send_from_directory("static",filename)
