import socket
import struct
from scapy.all import *
import time
import threading
#from __future__ import print_function


def get_multiplier(data):
    if int(data[0]) == 1:
        freq_check(parsData[1], 0, parsData[2], parsData, 1)
        volt_check(parsData[1], 0, 5000, parsData[2], 1)
    raise ValueError('Undefined unit: {}'.format(data))
 

       
def freq_check(time, flag ,freq,data_f_pmu , num_of_pmu):
    """
    freq function checking the frequency of each PMU station. 
    If received flag equal to 0 it means that PMU station don't have any anomaly before, 
    if flag equal to 1 it's mean anomaly received and extra check if anomaly are required,
    after 50ms it's mean CYBER ATACK 
    """
    if(flag == 0):
        if((freq - data_f_pmu[2]) > (freq * 0.01) or (freq - data_f_pmu[2]) < (freq * 0.01)):
            return [int(data_f_pmu[0]), 1, data_f_pmu[1]]
# returns data: 1 - PMU number, 2 - flag, 3 - time stamp
    if(flag == 1 and num_of_pmu == int(data_f_pmu[0])):
        if((time + data_f_pmu[1]) > (time + 0.05)):
            if((freq - data_f_pmu[2]) > (freq * 0.01) or (freq - data_f_pmu[2]) < (freq * 0.01)):
                print("CYBER ATTACK")
        else:
            if((freq - data_f_pmu[2]) > (freq * 0.01) or (freq - data_f_pmu[2]) < (freq * 0.01)):
                return [int(data_f_pmu[0]), 1, time]
            else:
                return [int(data_f_pmu[0]) , 0 , 0 ]
 
 
def volt_check(time, flag ,volt, data_f_pmu , num ):
    if(flag == 0):
        if(((volt - data_f_pmu[3]) > (volt * 0.05) or (volt - data_f_pmu[3]) < (volt * 0.1)) or
           ((volt - data_f_pmu[5]) > (volt * 0.05) or (volt - data_f_pmu[5]) < (volt * 0.1)) or
           ((volt - data_f_pmu[7]) > (volt * 0.05) or (volt - data_f_pmu[7]) < (volt * 0.1))):
            return [int(data_f_pmu[0]), 1, data_f_pmu[1]]
    if(flag == 1 and num == int(data_f_pmu[0])):
        if((time + data_f_pmu[1]) > (time + 10)):
            if(((volt - data_f_pmu[3]) > (volt * 0.05) or (volt - data_f_pmu[3]) < (volt * 0.1)) or
               ((volt - data_f_pmu[5]) > (volt * 0.05) or (volt - data_f_pmu[5]) < (volt * 0.1)) or
               ((volt - data_f_pmu[7]) > (volt * 0.05) or (volt - data_f_pmu[7]) < (volt * 0.1))):
                print("CYBER ATTACK")
        else:
            if(((volt - data_f_pmu[3]) > (volt * 0.05) or (volt - data_f_pmu[3]) < (volt * 0.1)) or
               ((volt - data_f_pmu[5]) > (volt * 0.05) or (volt - data_f_pmu[5]) < (volt * 0.1)) or
               ((volt - data_f_pmu[7]) > (volt * 0.05) or (volt - data_f_pmu[7]) < (volt * 0.1))):
                return [int(data_f_pmu[0]), 1, time]
            else:
                return [int(data_f_pmu[0]) , 0 , 0 ]
 
 
def amper_check(time, flag, data_f_pmu, line, num ):
    listVA = []
    listVB = []
    listVC = []
    vaComSum = 0
    vaSinSum = 0
    vbComSum = 0
    vbSinSum = 0
    vcComSum = 0
    vcSinSum = 0
 
    for i in range(3,45,6):
        listVA.append(data_f_pmu[i])
        listVA.append(data_f_pmu[i+1])
     
    for i in range(5,45,6):
        listVB.append(data_f_pmu[i])
        listVB.append(data_f_pmu[i+1])
     
    for i in range(7,45,6):
        listVC.append(data_f_pmu[i])
        listVC.append(data_f_pmu[i+1])
 
    if(flag == 0):
                #block of VA check
        for check in range(2,14,2):
            vaComSum += abs(listVA[0])*abs(listVA[check])*math.cos(math.radians(listVA[1])-(math.radians(listVA[check+1])))
        if(vaComSum > 0.00001):
            return [int(data_f_pmu[0]), 1, time , 11 ]
        for check in range(2,14,2):
            vaSinSum += abs(listVA[0])*abs(listVA[check])*math.sin(math.radians(listVA[1])-(math.radians(listVA[check+1])))
        if(vaSinSum > 0.00001):
            return [int(data_f_pmu[0]), 1, time , 12 ]
        for check in range(2,14,2):
            vbComSum += abs(listVA[0])*abs(listVA[check])*math.cos(math.radians(listVA[1])-(math.radians(listVA[check+1])))
        if(vbComSum > 0.00001):
            return [int(data_f_pmu[0]), 1, time , 21 ]
        for check in range(2,14,2):
            vbSinSum += abs(listVA[0])*abs(listVA[check])*math.sin(math.radians(listVA[1])-(math.radians(listVA[check+1])))
        if(vbSinSum > 0.00001):
            return [int(data_f_pmu[0]), 1, time , 22 ]
        for check in range(2,14,2):
            vcComSum += abs(listVA[0])*abs(listVA[check])*math.cos(math.radians(listVA[1])-(math.radians(listVA[check+1])))
        if(vcComSum > 0.00001):
            return [int(data_f_pmu[0]), 1, time , 31 ]
        for check in range(2,14,2):
            vcSinSum += abs(listVA[0])*abs(listVA[check])*math.sin(math.radians(listVA[1])-(math.radians(listVA[check+1])))
        if(vcSinSum > 0.00001):
            return [int(data_f_pmu[0]), 1, time , 32 ]    



UDP_IP = "127.0.0.1"
UDP_PORT = 1410

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
global_pars_xml =[[] for i in range(20)]
global_lists_of_freq = [[] for i in range(12)]  #length of list equal to number of pmu and for each one "time""flag""num_of_pmu"
global_lists_of_volt = [[] for i in range(12)]  
global_lists_of_amper = [[] for i in range(12)]            
            
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    len1 = len(data)
    parsData = struct.unpack('45d', data)
    print(parsData)
    if int(data[0]) == 1:
        freq_check(global_lists_of_freq[0], global_lists_of_freq[1], parsData[2], parsData, global_lists_of_freq[2])
        volt_check(parsData[1], 0, 5000, parsData[2], 1)
    if int(data[0]) == 2:
        freq_check(parsData[1], 0, parsData[2], parsData, 1)
        volt_check(parsData[1], 0, 5000, parsData[2], 1)
    if int(data[0]) == 3:
        freq_check(parsData[1], 0, parsData[2], parsData, 1)
        volt_check(parsData[1], 0, 5000, parsData[2], 1)
    if int(data[0]) == 4:
        freq_check(parsData[1], 0, parsData[2], parsData, 1)
        volt_check(parsData[1], 0, 5000, parsData[2], 1)
    raise ValueError('Undefined unit: {}'.format(data))
#     try:
#         t = threading.Thread(target = get_multiplier ,args = (parsData,))
#         t.start()
#     except:
#         print ("Error: unable to start thread")           