
# coding: utf-8

# In[22]:


import pandas as pd
import datetime

def parking_charge(output_csv_file):
    
    scenes_list = pd.read_csv(output_csv_file,skiprows=[0])


    in_time = scenes_list.loc[scenes_list['Scene Number'] == 1]

    In_time = pd.to_datetime(in_time['Start Timecode'], errors = 'coerce')

    out_time = max(list(scenes_list['End Timecode']))


    Out_time = pd.to_datetime(out_time,errors='coerce')

    Parkeduration = Out_time - In_time

    #print("Duration the car was parked", Parkeduration)

    with open("output/metadata.txt") as f:
        content = f.readlines()

    creation_date_time_ex = content[len(content)-2]
    creation_date_time_ex = creation_date_time_ex.split("=")[1].strip()

    creation_date,creation_time = creation_date_time_ex.split("T")

    creation_time,_ = creation_time.split("-")

    #creation_time

    Entrytime = pd.to_timedelta(creation_time)

    Exittime = Entrytime + Parkeduration

    
    
    entry = str(Entrytime).split(' ')[2]
   
    exit = str(Exittime).split(' ')[3].split('\n')[0]

    PD_insecs = (Parkeduration.astype('timedelta64[s]')).astype(int)


    PD_mins = (PD_insecs/60).astype(int)

    PD_hrs = (PD_mins/60).astype(int)

    if PD_hrs.item() > 0:
        Charge = PD_hrs.mul(1.5)
    else:
        Charge = 1.5

    print("Parking Charge is:",Charge,"$")
    
    return entry,exit,creation_date,Charge

