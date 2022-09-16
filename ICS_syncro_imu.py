import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory_ICS = '/home/yana/Рабочий стол/НС_15-09-22/данные_в_csv/окулограф_ICS/V1_2022_09_15_20_58_22.csv'
df_ICS = pd.read_csv(directory_ICS)

directory_imu1 = '/home/yana/Рабочий стол/НС_15-09-22/данные_в_csv/Инерциалки/правое/V1_imu1.csv'
directory_imu2 = '/home/yana/Рабочий стол/НС_15-09-22/данные_в_csv/Инерциалки/левое/V1_imu2.csv'

df_imu1 = pd.read_csv(directory_imu1)
df_imu2 = pd.read_csv(directory_imu2)

time_ics = np.array(df_ICS['Time'][:])
hor = np.array(df_ICS['Hor_eye'][:])
ver = np.array(df_ICS['Ver_eye'][:])


g1 = np.array(df_imu1[['gx', 'gy', 'gz']])
g2 = np.array(df_imu2[['gx', 'gy', 'gz']])

a1 = np.array(df_imu1[['ax', 'ay', 'az']])
a2 = np.array(df_imu2[['ax', 'ay', 'az']])
time_imu1 = df_imu1['server_time'][:]
# time_imu2 = df_imu2['server_time'][:]

# время инерциалок
seconds_imu = []
for j in range(len(time_imu1)):
    time_j = time_imu1[j][-15:-1].split(':')
    seconds_imu.append(int(time_j[0])*60*60 + int(time_j[1])*60 + float(time_j[2]))

# обрезаем начало
seconds_imu = np.array(seconds_imu)
i = 0
if min(time_ics) > min(seconds_imu):
    while seconds_imu[i] < time_ics[0]:
        seconds_imu = np.delete(seconds_imu, i)
        g1 = np.delete(g1, i, 0)
        g2 = np.delete(g2, i, 0)
        a1 = np.delete(a1, i, 0)
        a2 = np.delete(a2, i, 0)
if min(time_ics) < min(seconds_imu):
    while time_ics[i] < seconds_imu[0]:
        time_ics = np.delete(time_ics, i)
        hor = np.delete(hor, i)
        ver = np.delete(ver, i)

# обрезаем конец
j = -1
if max(time_ics) > max(seconds_imu):
    while time_ics[j] > seconds_imu[-1]:
        time_ics = np.delete(time_ics, j)
        hor = np.delete(hor, j)
        ver = np.delete(ver, j)

if max(time_ics) < max(seconds_imu):
    while seconds_imu[j] > time_ics[-1]:
        seconds_imu = np.delete(seconds_imu, j)
        g1 = np.delete(g1, j, 0)
        g2 = np.delete(g2, j, 0)
        a1 = np.delete(a1, j, 0)
        a2 = np.delete(a2, j, 0)

# расширенный массив времени
all_time = np.concatenate((time_ics, seconds_imu), axis=0)
# all_time = time_ics + seconds_imu
all_time.sort()
start = all_time[0]

# print(np.array(all_time).reshape(len(all_time), 1))
# a = [1,2,3,4,5]
# b = [1,2,3,4,5]
# print(np.concatenate((a,b)).reshape(2,5))

# функция дополняет данные массива измерений в новых точках расширенного времени предыдущим ненулевым измерением
def long_func(g, seconds_imu,  all_time):
    g_long = []
    buf = g[0]
    j = 0

    for i in range(len(all_time)):
        if all_time[i] == seconds_imu[j]:
            g_long.append(g[j])
            buf = g[j]
            if j != len(seconds_imu)-1:
                j += 1
        else:
            g_long.append(buf)
    return g_long

g1_long = long_func(g1, seconds_imu, all_time)
g2_long = long_func(g2, seconds_imu, all_time)
a1_long = long_func(a1, seconds_imu, all_time)
a2_long = long_func(a2, seconds_imu, all_time)
hor_long = long_func(hor, time_ics, all_time)
ver_long = long_func(ver, time_ics, all_time)

# print(len(g1_long), len(hor_ver_long))
# print(len(all_time))
all_time = np.array(all_time).reshape(len(all_time),1)
g1_long = np.array(g1_long)
g2_long = np.array(g2_long)
a1_long = np.array(a1_long)
a2_long = np.array(a2_long)
hor_long = np.array(hor_long).reshape(len(all_time),1)
ver_long = np.array(ver_long).reshape(len(all_time),1)

ocu = np.hstack([all_time, hor_long])
ocu = np.hstack([ocu, ver_long])


g = np.hstack([g1_long, g2_long])
a = np.hstack([a1_long, a2_long])
imu = np.hstack([g, a])
data = np.hstack([ocu, imu])

# print(data)
# # print(data)
# # g1x = g1_long[:,0]
#
# columns = ['Time', 'Hor_eye', 'Ver_eye', 'imu1_gx', 'imu1_gy', 'imu1_gz',  'imu2_gx', 'imu2_gy', 'imu2_gz',
#            'imu1_ax', 'imu1_ay', 'imu1_az',  'imu2_ax', 'imu2_ay', 'imu2_az']
#
# df = pd.DataFrame(data, columns=columns)
# df.to_csv(r'/home/yana/Рабочий стол/НС_15-09-22/data_set/NN_Y2_data1.csv')


# # a = [1,2,3,4,5]
# # b = [1,2,3,4,5]
# # print(np.concatenate((a,b)).reshape(2,5))
#
fig = plt.figure(figsize=(10,5))
plot_1 = fig.add_subplot(2,1,1)
plot_2 = fig.add_subplot(2,1,2)


plot_1.plot(all_time, hor_long, '.', markersize = 1, color = "orange", label = 'Ver')
plot_1.plot(all_time, ver_long, '.', markersize = 3, color = "green", label = 'Hor')
#
# # plot_1.plot(ax2, '.', markersize = 1, color = "orange", label = 'Ver')
# # plot_1.plot(ay2, '.', markersize = 3, color = "green", label = 'Hor')
# # plot_1.plot(az2, '.', markersize = 3, color = "red", label = 'Hor')
# #
# # plot_2.plot(gx2, '.', markersize = 1, color = "orange", label = 'Ver')
# # plot_2.plot(gy2, '.', markersize = 3, color = "green", label = 'Hor')
# # plot_2.plot(gz2, '.', markersize = 3, color = "red", label = 'Hor')
#
# # plot_1.plot(a1[:,0], '.', markersize = 1, color = "orange", label = 'Ver')
# # plot_1.plot(a1[:,1], '.', markersize = 3, color = "green", label = 'Hor')
# # plot_1.plot(a1[:,2], '.', markersize = 3, color = "red", label = 'Hor')
#
plot_2.plot(all_time, g1_long, '.', markersize = 1)
# # plot_2.plot(seconds_imu, g1_long[:,1], '.', markersize = 3, color = "green", label = 'Hor')
# # plot_2.plot(seconds_imu, g1_long[:,2], '.', markersize = 3, color = "red", label = 'Hor')
# #
plot_1.grid()
plot_2.grid()
#
plt.show()
