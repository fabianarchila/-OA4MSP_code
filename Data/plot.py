import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.patches as patches

from scipy.interpolate import interp1d



## For lidar data functions

def from_gps_to_meters(original,gps):
    earth_radius=6378137.0
    newlat_in = earth_radius*(np.pi/180)*(gps[0]-original[0])
    newlon_in = (earth_radius*np.cos(np.pi*original[0]/180))*(np.pi/180)*(gps[1]-original[1])
    return np.array([newlon_in,newlat_in])


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

####################################################################

leader_1 = np.load("proced_data/1_1.npy")
leader_2 = np.load("proced_data/1_2.npy")
leader_3 = np.load("proced_data/1_3.npy")
leader_4 = np.load("proced_data/1_4.npy")
leader_5 = np.load("proced_data/1_5.npy")
leader_6 = np.load("proced_data/1_6.npy")

follower2_1 = np.load("proced_data/2_1.npy")
follower2_2 = np.load("proced_data/2_2.npy")
follower2_3 = np.load("proced_data/2_3.npy")
follower2_4 = np.load("proced_data/2_4.npy")
follower2_5 = np.load("proced_data/2_5.npy")
follower2_6 = np.load("proced_data/2_6.npy")

follower3_1 = np.load("proced_data/3_1.npy")
follower3_2 = np.load("proced_data/3_2.npy")
follower3_3 = np.load("proced_data/3_3.npy")
follower3_4 = np.load("proced_data/3_4.npy")
follower3_5 = np.load("proced_data/3_5.npy")
follower3_6 = np.load("proced_data/3_6.npy")


leader_x = [leader_1[0],leader_2[0],leader_3[0],leader_4[0],leader_5[0],leader_6[0]]
leader_y = [leader_1[1],leader_2[1],leader_3[1],leader_4[1],leader_5[1],leader_6[1]]
leader_t = [leader_1[2],leader_2[2],leader_3[2],leader_4[2],leader_5[2],leader_6[2]]

common_t = np.linspace(0,80,2000)

leader_x_int = []
for x, y in zip(leader_t, leader_x):
    interp_func = interp1d(x, y, kind='cubic', fill_value="extrapolate")  # Cubic interpolation
    leader_x_int.append(interp_func(common_t))  # Interpolated values

leader_y_int = []
for x, y in zip(leader_t, leader_y):
    interp_func = interp1d(x, y, kind='cubic', fill_value="extrapolate")  # Cubic interpolation
    leader_y_int.append(interp_func(common_t))  # Interpolated values


leader_x_mean = np.mean(leader_x_int, axis=0)
leader_y_mean = np.mean(leader_y_int, axis=0)

leader_x_std = np.std(leader_x_int, axis=0)
leader_y_std = np.std(leader_y_int, axis=0)



follower2_x = [follower2_1[0],follower2_2[0],follower2_3[0],follower2_4[0],follower2_5[0],follower2_6[0]]
follower2_y = [follower2_1[1],follower2_2[1],follower2_3[1],follower2_4[1],follower2_5[1],follower2_6[1]]
follower2_t = [follower2_1[2],follower2_2[2],follower2_3[2],follower2_4[2],follower2_5[2],follower2_6[2]]


follower2_x_int = []
for x, y in zip(follower2_t, follower2_x):
    interp_func = interp1d(x, y, kind='cubic', fill_value="extrapolate")  # Cubic interpolation
    follower2_x_int.append(interp_func(common_t))  # Interpolated values

follower2_y_int = []
for x, y in zip(follower2_t, follower2_y):
    interp_func = interp1d(x, y, kind='cubic', fill_value="extrapolate")  # Cubic interpolation
    follower2_y_int.append(interp_func(common_t))  # Interpolated values


follower2_x_mean = np.mean(follower2_x_int, axis=0)
follower2_y_mean = np.mean(follower2_y_int, axis=0)

follower2_x_std = np.std(follower2_x_int, axis=0)
follower2_y_std = np.std(follower2_y_int, axis=0)


follower3_x = [follower3_1[0],follower3_2[0],follower3_3[0],follower3_4[0],follower3_5[0],follower3_6[0]]
follower3_y = [follower3_1[1],follower3_2[1],follower3_3[1],follower3_4[1],follower3_5[1],follower3_6[1]]
follower3_t = [follower3_1[2],follower3_2[2],follower3_3[2],follower3_4[2],follower3_5[2],follower3_6[2]]


follower3_x_int = []
for x, y in zip(follower3_t, follower3_x):
    interp_func = interp1d(x, y, kind='cubic', fill_value="extrapolate")  # Cubic interpolation
    follower3_x_int.append(interp_func(common_t))  # Interpolated values

follower3_y_int = []
for x, y in zip(follower3_t, follower3_y):
    interp_func = interp1d(x, y, kind='cubic', fill_value="extrapolate")  # Cubic interpolation
    follower3_y_int.append(interp_func(common_t))  # Interpolated values


follower3_x_mean = np.mean(follower3_x_int, axis=0)
follower3_y_mean = np.mean(follower3_y_int, axis=0)

follower3_x_std = np.std(follower3_x_int, axis=0)
follower3_y_std = np.std(follower3_y_int, axis=0)




# print(leader_1[2,-1])
# print(leader_2[2,-1])
# print(leader_3[2,-1])
# print(leader_4[2,-1])
# print(leader_5[2,-1])
# print(leader_6[2,-1])



# print(follower2_1[2,-1])
# print(follower2_2[2,-1])
# print(follower2_3[2,-1])
# print(follower2_4[2,-1])
# print(follower2_5[2,-1])
# print(follower2_6[2,-1])

# print(follower3_1[2,-1])
# print(follower3_2[2,-1])
# print(follower3_3[2,-1])
# print(follower3_4[2,-1])
# print(follower3_5[2,-1])
# print(follower3_6[2,-1])

figure, axes = plt.subplots()



for i in range(0,len(leader_x_std)):
    if i == 0:
        rectangle1 = patches.Rectangle((leader_x_mean[i]-leader_x_std[i], leader_y_mean[i]-leader_y_std[i]), 2*leader_x_std[i], 2*leader_y_std[i], facecolor='#e39889', alpha=1, edgecolor = None,label = 'Leader standard deviation')
        axes.add_patch(rectangle1)
        rectangle2 = patches.Rectangle((follower2_x_mean[i]-follower2_x_std[i], follower2_y_mean[i]-follower2_y_std[i]), 2*follower2_x_std[i], 2*follower2_y_std[i], facecolor='#adc3e9', alpha=1, edgecolor = None,label = 'Follower 1 standard deviation')
        axes.add_patch(rectangle2)
        rectangle3 = patches.Rectangle((follower3_x_mean[i]-follower3_x_std[i], follower3_y_mean[i]-follower3_y_std[i]), 2*follower3_x_std[i], 2*follower3_y_std[i], facecolor='#b3f399', alpha=1, edgecolor = None,label = 'Follower 2 standard deviation')
        axes.add_patch(rectangle3)
        #7a956f
    else:
        rectangle = patches.Rectangle((leader_x_mean[i]-leader_x_std[i], leader_y_mean[i]-leader_y_std[i]), 2*leader_x_std[i], 2*leader_y_std[i], facecolor='#e39889', alpha=1, edgecolor = None)
        axes.add_patch(rectangle)
        rectangle = patches.Rectangle((follower2_x_mean[i]-follower2_x_std[i], follower2_y_mean[i]-follower2_y_std[i]), 2*follower2_x_std[i], 2*follower2_y_std[i], facecolor='#adc3e9', alpha=1, edgecolor = None)
        axes.add_patch(rectangle)
        rectangle = patches.Rectangle((follower3_x_mean[i]-follower3_x_std[i], follower3_y_mean[i]-follower3_y_std[i]), 2*follower3_x_std[i], 2*follower3_y_std[i], facecolor='#b3f399', alpha=1, edgecolor = None)
        axes.add_patch(rectangle)

    # Add rectangle to the plot
    
p2 = 500
p3 = 1300

color_initial = "#6b2323"
color_final = "#545454"
h1, = plt.plot(leader_x_mean,leader_y_mean,label="Average leader",color = "#e34321")
b1, =plt.plot(leader_x_mean[0],leader_y_mean[0],'o',color = color_initial, label ="Initial position")
b2, = plt.plot(leader_x_mean[-1],leader_y_mean[-1],'*',color = color_final,label = "Final position")
# plt.plot(leader_x_mean[p2],leader_y_mean[p2],'o',color = "#e34321")
# plt.plot(leader_x_mean[p3],leader_y_mean[p3],'o',color = "#e34321")
h2,=plt.plot(follower2_x_mean,follower2_y_mean,label="Average follower 1", color = "#216ae3")
plt.plot(follower2_x_mean[0],follower2_y_mean[0],'o', color = color_initial)
plt.plot(follower2_x_mean[-1],follower2_y_mean[-1],'*', color = color_final)
# plt.plot(follower2_x_mean[p2],follower2_y_mean[p2],'o', color = "#216ae3")
# plt.plot(follower2_x_mean[p3],follower2_y_mean[p3],'o', color = "#216ae3")
h3,=plt.plot(follower3_x_mean,follower3_y_mean,label="Average follower 2",color = "#368f13")
plt.plot(follower3_x_mean[0],follower3_y_mean[0],'o',color = color_initial)
plt.plot(follower3_x_mean[-1],follower3_y_mean[-1],'*',color = color_final)
# plt.plot(follower3_x_mean[p2],follower3_y_mean[p2],'o',color = "#368f13")
# plt.plot(follower3_x_mean[p3],follower3_y_mean[p3],'o',color = "#368f13")




##########################Lidar code

data_ros_scan=np.load("lidar_data.npy")
time_ros_scan=np.load("lidar_time.npy")
data_ros_pos=np.load("pos_data.npy")
time_ros_pos = np.load("pos_time.npy")


lidar_k_samples=np.zeros(len(data_ros_pos))
for i in range(0,len(lidar_k_samples)):
    temp_index=find_closest_index(time_ros_scan,time_ros_pos[i])
    lidar_k_samples[i]=temp_index


zero = np.array([51.769090, 14.323523, 5])

data_3_converter=np.zeros([len(data_ros_pos),2])

for i in range(0,len(data_ros_pos)):
    data_3_converter[i]=from_gps_to_meters(zero,np.array([data_ros_pos[i,0],data_ros_pos[i,1],5]))


init=0.25 #percentages
final = 0.3

init_i=int(init*len(data_ros_pos))
final_i=int(final*len(data_ros_pos))


in_temp =0
for i in range(init_i, final_i):
    increment=0.007853981633974483#0.015747331082820892
    pos_meters=data_3_converter[i]
    rotation = 5*(2*np.pi/360)#np.pi/2
    data_in_temp=data_ros_scan[int(lidar_k_samples[i])]
    for j in range(len(data_ros_scan[int(lidar_k_samples[i]),:])):
        if data_in_temp[j]*np.sin(increment*(j+1)-rotation)+pos_meters[1]<-12.5:
            if in_temp==0:
                li, = plt.plot(data_in_temp[j]*np.cos(increment*(j+1)-rotation)+pos_meters[0],data_in_temp[j]*np.sin(increment*(j+1)-rotation)+pos_meters[1],'2',color="#2f3e46",label="LIDAR data")
                in_temp=1
            else:
                plt.plot(data_in_temp[j]*np.cos(increment*(j+1)-rotation)+pos_meters[0],data_in_temp[j]*np.sin(increment*(j+1)-rotation)+pos_meters[1],'2',color="#2f3e46")




axes.set_aspect( 1 )
axes.legend(loc='upper right',fontsize = 'xx-small',handles=[h1, h2, h3, rectangle1, rectangle2, rectangle3,b1,b2,li])
plt.xlim([-43,8])
plt.ylim([-22,31])
#plt.ylim([-16,27])
#plt.xlim([0,20])
#plt.ylim([0,10])
plt.xlabel('x (m)')
plt.ylabel('y (m)')
#plt.savefig('final_f.pdf',format='pdf',pad_inches=0,bbox_inches='tight')
plt.show()


figure1, (axes1,axes2) = plt.subplots(2,1)

axes1.plot(common_t,leader_x_mean,label = r'$x_{L}$'+ " average", color ="#e34321")
axes1.plot(common_t,follower2_x_mean, label = r'$x_{F1}$'+ " average", color = "#216ae3")
axes1.plot(common_t,follower3_x_mean, label = r'$x_{F2}$'+ " average", color ="#368f13")



axes1.fill_between(common_t, leader_x_mean - leader_x_std, leader_x_mean + leader_x_std, color='#e34321', alpha=0.2, label="standard deviation "+r'$x_{L}$')
axes1.fill_between(common_t, follower2_x_mean - follower2_x_std, follower2_x_mean + follower2_x_std, color='#216ae3', alpha=0.2, label="standard deviation "+r'$x_{F1}$')
axes1.fill_between(common_t, follower3_x_mean - follower3_x_std, follower3_x_mean + follower3_x_std, color='#368f13', alpha=0.2, label="standard deviation "+r'$x_{F2}$')

axes1.set_ylabel("y (m)")
axes1.legend(loc='lower right',fontsize = 'xx-small')
axes1.grid(True)



axes2.plot(common_t,leader_y_mean,label = r'$y_{L}$'+ " average", color ="#e34321")
axes2.plot(common_t,follower2_y_mean, label = r'$y_{F1}$'+ " average", color = "#216ae3")
axes2.plot(common_t,follower3_y_mean, label = r'$y_{F2}$'+ " average", color ="#368f13")

axes2.fill_between(common_t, leader_y_mean - leader_y_std, leader_y_mean + leader_y_std, color='#e34321', alpha=0.2, label="standard deviation "+r'$y_{L}$')
axes2.fill_between(common_t, follower2_y_mean - follower2_y_std, follower2_y_mean + follower2_y_std, color='#216ae3', alpha=0.2, label="standard deviation "+r'$y_{F1}$')
axes2.fill_between(common_t, follower3_y_mean - follower3_y_std, follower3_y_mean + follower3_y_std, color='#368f13', alpha=0.2, label="standard deviation "+r'$y_{F2}$')



axes2.legend(loc='upper left',fontsize = 'xx-small')
axes2.grid(True)
plt.xlabel("t (s)")
plt.ylabel("x (m)")
plt.savefig('final_time.pdf',format='pdf',pad_inches=0,bbox_inches='tight')

plt.show()


