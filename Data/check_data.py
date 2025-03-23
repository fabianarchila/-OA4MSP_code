import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches



def find_closest_index(arr, value):
    """
    Find the index of the given value in the array.
    If the exact value is not found, return the index of the closest value.
    
    Parameters:
        arr (numpy.ndarray): Input array.
        value (float or int): Value to find.
    
    Returns:
        int: Index of the exact or closest value.
    """
    arr = np.asarray(arr)  # Ensure input is a NumPy array
    index = np.argmin(np.abs(arr - value))  # Find the index of the closest value
    return index

def from_gps_to_meters(original,gps):
    earth_radius=6378137.0
    newlat_in = earth_radius*(np.pi/180)*(gps[0]-original[0])
    newlon_in = (earth_radius*np.cos(np.pi*original[0]/180))*(np.pi/180)*(gps[1]-original[1])
    return np.array([newlon_in,newlat_in])



time_exp = 75 


gps=pd.read_csv("3_2_gps_t.csv",header=None)
gps.reset_index(drop=True)
gps_temp = np.array(gps[0]) 
gps = np.array([gps_temp[0:int(len(gps_temp)/3)],gps_temp[int(len(gps_temp)/3):int(2*len(gps_temp)/3)],gps_temp[int(2*len(gps_temp)/3):int(len(gps_temp))]])




pos=pd.read_csv("3_2_pos_t.csv",header=None)
pos.reset_index(drop=True)
pos_temp = np.array(pos[0])
pos = np.array([pos_temp[0:int(len(pos_temp)/3)],pos_temp[int(len(pos_temp)/3):int(2*len(pos_temp)/3)],pos_temp[int(2*len(pos_temp)/3):int(len(pos_temp))]])





print("Time in weeks format is for gps globals {}".format(gps[2,10]))


index =  find_closest_index(gps[2,:],394182600)
print("The closer index is {} and the value is {}".format(index,gps[2,index]))

start_possible = gps[2,index]/1000-gps[2,0]/1000
print("Possible start in seconds {}".format(start_possible))


data_time_gps = (gps[2]-gps[2,0])/1000
data_time_pos = (pos[2]-pos[2,0])/1000000

total_time = data_time_gps[-1]

print("Total time is {}".format(total_time))

t_inicial = 319.2-10# -10
t_final = t_inicial + 80 # +80

index_init_gps =  find_closest_index(data_time_gps,t_inicial)
index_final_gps =  find_closest_index(data_time_gps,t_final)


index_init_pos =  find_closest_index(data_time_pos,t_inicial)
index_final_pos =  find_closest_index(data_time_pos,t_final)

print(index_init_gps)
print(index_final_gps)
print(index_init_pos)
print(index_final_pos)

print("Index is {} and global is {} ".format(index_init_gps, gps[2,index_init_gps]))

interval = np.array([index_init_gps, index_final_gps])
interval_2 = np.array([index_init_pos,index_final_pos])


zero = np.array([51.769090, 14.323523, 5])

data1_converter=np.zeros([len(gps[0]),2])
data2_converter=np.zeros([len(pos[0]),2])

for i in range(0,len(gps[0])):

    data1_converter[i]=from_gps_to_meters(zero,np.array([gps[0,i],gps[1,i],5]))

for i in range(0,len(pos[0])):
    data2_converter[i]=from_gps_to_meters(zero,np.array([pos[0,i],pos[1,i],5]))





data_temp = np.array([data2_converter[interval_2[0]:interval_2[1],0],data2_converter[interval_2[0]:interval_2[1],1],data_time_pos[interval_2[0]:interval_2[1]]-data_time_pos[interval_2[0]]])
print(data_temp)
# np.save("proced_data/3_6",data_temp)
# print(data_temp)
figure, axes = plt.subplots()
plt.plot(data1_converter[interval[0]:interval[1],0],data1_converter[interval[0]:interval[1],1],color ='#365E32',label = "GPS")
plt.plot(data2_converter[interval_2[0]:interval_2[1],0],data2_converter[interval_2[0]:interval_2[1],1],color ='#FD9B63',label = "POS")
axes.set_aspect( 1 )
plt.legend()
#plt.xlim([0,20])
#plt.ylim([0,10])
plt.show()