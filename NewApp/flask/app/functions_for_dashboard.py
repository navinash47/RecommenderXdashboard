def plugin_csv(name,phone_no,from_date,to_date,file_name):

    import pandas as pd
    import numpy as ny
    #take data from influx db
    df=pd.read_csv('dummy.csv')
    from datetime import date, timedelta
    test=[]
    test.append(phone_no)
    df1=df.loc[df['Phone']==ny.int64(phone_no)]
    
    #
    f_date_split=from_date.split("-")
    t_date_split=to_date.split("-")
    sdate = date(int(f_date_split[0]), int(f_date_split[1]), int(f_date_split[2]))   # start date
    edate = date(int(t_date_split[0]), int(t_date_split[1]), int(t_date_split[2]))   # end date

    delta = edate - sdate       # as timedelta
    days=[]
    dd=""
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        days.append(str(day))
    
    df1=df1.loc[df['time'].isin(days)]
    path="app/static/"+file_name
    path_file=r"{}".format(path)
    df1.to_csv(path_file,index=False)
    return "Working"


def plugin_check_cred(name,phone_no):
    import pandas as pd
    import numpy as ny
    #take data from influx db
    df = pd.read_csv("dummy.csv")

    df=df.loc[df["Phone"]==ny.int64(phone_no)]
    df=df.loc[df["Name"]==name]

    if(len(df)==0):
        return False
    else:
        return True
