# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 7/15/2016 11:47:39 AM
Last modified: Wed 06 Jun 2018 06:55:46 AM CEST
"""

#defaut setting for scientific caculation
#import numpy
#import scipy
#from numpy import *
#import numpy as np
#import scipy as sp
#import pylab as pl
#from openpyxl import Workbook
import numpy as np
import struct
import os
from sys import exit
import os.path
import copy

def rawto32chn(onepkgdata, chn_data):
    i = 0
    if (onepkgdata[i] == 0xface ) or (onepkgdata[i] == 0xfeed ):
        if (onepkgdata[i] == 0xface ):
            pre = 0x00000
        elif(onepkgdata[i] == 0xfeed ):
            pre = 0x10000
        chn_data[7].append( pre + ((onepkgdata[i+1] & 0X0FFF)<<0 ))
        chn_data[6].append( pre + ((onepkgdata[i+2] & 0X00FF)<<4)+ ((onepkgdata[i+1] & 0XF000) >> 12))
        chn_data[5].append( pre + ((onepkgdata[i+3] & 0X000F)<<8) +((onepkgdata[i+2] & 0XFF00) >> 8 ))
        chn_data[4].append( pre + ((onepkgdata[i+3] & 0XFFF0)>>4 ))

        chn_data[3].append( pre + ( onepkgdata[i+3+1] & 0X0FFF)<<0 )
        chn_data[2].append( pre + ((onepkgdata[i+3+2] & 0X00FF)<<4) + ((onepkgdata[i+3+1] & 0XF000) >> 12))
        chn_data[1].append( pre + ((onepkgdata[i+3+3] & 0X000F)<<8) + ((onepkgdata[i+3+2] & 0XFF00) >> 8 ))
        chn_data[0].append( pre + ((onepkgdata[i+3+3] & 0XFFF0)>>4) )

        chn_data[15].append(pre +  ((onepkgdata[i+6+1] & 0X0FFF)<<0 ))
        chn_data[14].append(pre +  ((onepkgdata[i+6+2] & 0X00FF)<<4 )+ ((onepkgdata[i+6+1] & 0XF000) >> 12))
        chn_data[13].append(pre +  ((onepkgdata[i+6+3] & 0X000F)<<8 )+ ((onepkgdata[i+6+2] & 0XFF00) >> 8 ))
        chn_data[12].append(pre +  ((onepkgdata[i+6+3] & 0XFFF0)>>4 ))

        chn_data[11].append(pre +  ((onepkgdata[i+9+1] & 0X0FFF)<<0 ))
        chn_data[10].append(pre +  ((onepkgdata[i+9+2] & 0X00FF)<<4 )+ ((onepkgdata[i+9+1] & 0XF000) >> 12))
        chn_data[9].append( pre +  ((onepkgdata[i+9+3] & 0X000F)<<8 )+ ((onepkgdata[i+9+2] & 0XFF00) >> 8 ))
        chn_data[8].append( pre +  ((onepkgdata[i+9+3] & 0XFFF0)>>4 ))


        chn_data[23].append(pre +  ((onepkgdata[12+i+1] & 0X0FFF)<<0 ))
        chn_data[22].append(pre +  ((onepkgdata[12+i+2] & 0X00FF)<<4)    +((onepkgdata[12+i+1] & 0XF000) >> 12))
        chn_data[21].append(pre +  ((onepkgdata[12+i+3] & 0X000F)<<8)    +((onepkgdata[12+i+2] & 0XFF00) >> 8 ))
        chn_data[20].append(pre +  ((onepkgdata[12+i+3] & 0XFFF0)>>4 ))

        chn_data[19].append(pre +  ( onepkgdata[12+i+3+1] & 0X0FFF)<<0 )
        chn_data[18].append(pre +  ((onepkgdata[12+i+3+2] & 0X00FF)<<4) + ((onepkgdata[12+i+3+1] & 0XF000) >> 12))
        chn_data[17].append(pre +  ((onepkgdata[12+i+3+3] & 0X000F)<<8) + ((onepkgdata[12+i+3+2] & 0XFF00) >> 8 ))
        chn_data[16].append(pre +  ((onepkgdata[12+i+3+3] & 0XFFF0)>>4) )

        chn_data[31].append(pre +  ((onepkgdata[12+i+6+1] & 0X0FFF)<<0 ))
        chn_data[30].append(pre +  ((onepkgdata[12+i+6+2] & 0X00FF)<<4 )+ ((onepkgdata[12+i+6+1] & 0XF000) >> 12))
        chn_data[29].append(pre +  ((onepkgdata[12+i+6+3] & 0X000F)<<8 )+ ((onepkgdata[12+i+6+2] & 0XFF00) >> 8 ))
        chn_data[28].append(pre +  ((onepkgdata[12+i+6+3] & 0XFFF0)>>4 ))

        chn_data[27].append(pre +  ((onepkgdata[12+i+9+1] & 0X0FFF)<<0 ))
        chn_data[26].append(pre +  ((onepkgdata[12+i+9+2] & 0X00FF)<<4 )+ ((onepkgdata[12+i+9+1] & 0XF000) >> 12))
        chn_data[25].append(pre +  ((onepkgdata[12+i+9+3] & 0X000F)<<8 )+ ((onepkgdata[12+i+9+2] & 0XFF00) >> 8 ))
        chn_data[24].append(pre +  ((onepkgdata[12+i+9+3] & 0XFFF0)>>4 ))

        cycle_del = False
    else:
        print ("ERROR")
        cycle_del = True
    i = i + 25 
    return chn_data ,cycle_del

def raw_convertor_conv(fp, jumbo_flag=True):
    if (jumbo_flag == True):
        pkg_len = int(0x1df4/2)
    else:
        pkg_len = int(0x3fa/2)
    with open(fp, 'rb') as f:
        raw_data = f.read()                
        len_file = len(raw_data) 
        dataNtuple =struct.unpack_from(">%dH"%(len_file//2),raw_data)

        addr = 0
        links_face_pos = [np.array([]), np.array([]), np.array([]), np.array([])]
        links_feed_pos = [np.array([]), np.array([]), np.array([]), np.array([])]
        link_i = 0
        while (addr <= len(dataNtuple) - 25 ):
            pkg_cnt0 = ((((dataNtuple[addr]) << 16 )+ (dataNtuple[addr+1])) ) & 0xFFFFFFFF
            pkg_res0 = ((((dataNtuple[addr+2]) << 16 )+ (dataNtuple[addr+3])) ) & 0xFFFFFFFF
            a = addr
            for b in range(addr, len(dataNtuple)-4, 1):
                #print (b)
                pkg_cnt1 = ((((dataNtuple[b]) << 16 )+ (dataNtuple[b+1])) ) & 0xFFFFFFFF
                pkg_res1 = ((((dataNtuple[b+2]) << 16 )+ (dataNtuple[b+3])) ) & 0xFFFFFFFF
                if (pkg_cnt1 == pkg_cnt0 + 1) and (pkg_res0 == 0) and (pkg_res1 == 0):
                    break 
            udp_pkg = np.array(dataNtuple[a:b])
            face_pos = np.where(udp_pkg == 0xface)[0]
            feed_pos = np.where(udp_pkg == 0xfeed)[0]  
            face_pos = np.sort( (np.append(face_pos, feed_pos))) + a
            feed_pos =  feed_pos + a
            addr = b
            links_face_pos[link_i] = np.append(links_face_pos[link_i] , face_pos)
            links_feed_pos[link_i] = np.append(links_feed_pos[link_i] , feed_pos)
            if (b-a) < pkg_len:
                link_i +=1
        link_data = [[],[],[],[]]
        for i in range(len(links_face_pos)):
            chn_data = []
            for x in range(32):
                chn_data.append([])
            for j in range(len(links_face_pos[i])-1):
                if (links_face_pos[i][j+1] - links_face_pos[i][j] == 25): 
                    onepkgdata = dataNtuple[int(links_face_pos[i][j]) : int(links_face_pos[i][j]) +25 ]
                    chn_data, cycle_del =  rawto32chn(onepkgdata, chn_data)
            link_data[i] = chn_data
        femb_data = link_data[0] + link_data[1] + link_data[2] + link_data[3] 
    return femb_data

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.mlab as mlab

def mk_plot(femb_data):
    for j in range(8):
        fig = plt.figure(figsize=(16,8))
        plt.rcParams.update({'font.size': 6})
        for i in range(16):
            chn = 16*j + i
            ax = plt.subplot2grid((8,2), (int(i%8), int(i//8)),  colspan=1, rowspan=1)
            x = np.arange(len(femb_data[chn])) * 0.5
            y = np.array(femb_data[chn])%0x10000
            ax.plot(x[0:150], y[0:150], marker = '.', label="CH%d"%chn)
            ax.set_ylim((1000, 3500))
            ax.set_xlabel("Time / us")
            ax.set_ylabel("ADC counts / LSB")
            ax.legend(loc = 1)
            ax.grid()

        plt.tight_layout()
        plt.show()
  #      plt.savefig(save_fp)
        plt.close()



fp = "/Users/shanshangao/Documents/tmp/run11tri/WIB00step18_FEMB0_B8_158580569657.bin"
fp = "/Users/shanshangao/Documents/tmp/run11tri/WIB00step18_FEMB0_B8_158580569681.bin"
fembdata = raw_convertor_conv(fp)
mk_plot(fembdata)
