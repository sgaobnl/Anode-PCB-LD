# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 7/15/2016 11:47:39 AM
Last modified: 3/1/2021 6:44:59 AM
"""
import matplotlib
matplotlib.use('Agg')
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
import sys
import os.path
import math
import pickle
from matplotlib.backends.backend_pdf import PdfPages

from apa_plot_out import load_sum
from apa_plot_out import plot0_overall_enc
from apa_plot_out import plot3_overall_gain
from apa_plot_out import plot2_peds
from apa_plot_out import plot1_chns_enc
from apa_plot_out import plot1_chns_enc_1
from apa_plot_out import plot4_chns_gain
from apa_plot_out import dict_filter
from apa_plot_out import dict_del_chn

APAno = 9
datafp = "./data_path.txt"
with open(datafp, 'r') as f:
    chk_path = f.readline().replace("\n", "")
    rms_path = f.readline().replace("\n", "")
    fpg_path = f.readline().replace("\n", "")
    asic_path = f.readline().replace("\n", "")

if (rms_path != "Void"):
    rms_pos = rms_path.find("Rawdata_")
    rms_rootpath =  rms_path[:rms_pos + 19]
    rmsrunno =  rms_path[rms_pos + 19:rms_pos + 19+8]
else:
    print ("Error, no RMS data is found!")

if (fpg_path != "Void"):
    fpg_pos = fpg_path.find("Rawdata_")
    fpga_rootpath =  fpg_path[:fpg_pos + 19]
    fpgarunno =  fpg_path[fpg_pos + 19:fpg_pos + 19+8]
else:
    print ("Error, no calibration data is found!")

if (asic_path != "Void"):
    asic_pos = asic_path.find("Rawdata_")
    asic_rootpath =  asic_path[:asic_pos + 19]
    asicrunno =  asic_path[asic_pos + 19:asic_pos + 19+8]
else:
    asic_rootpath = rms_rootpath
    asicrunno = "run99asi"

loc = 2
fembs_on_apa = [loc] 

sum_path = rms_rootpath + "results/" + "APA%d_"%APAno + rmsrunno + "_" + fpgarunno + "_" + asicrunno +"/"
fn = "APA%d"%APAno + "_" + rmsrunno + "_" + fpgarunno + "_" + asicrunno
orgdicts = load_sum (sum_path, fn + ".allsum")

femb_cs = []
for fembloc in fembs_on_apa:
    if (fembloc <= 10):
        femb_cs.append(["apaloc", "B" + format(APAno, "1d") + format(fembloc, "02d")])
    else:
        femb_cs.append(["apaloc", "A" + format(APAno, "1d") + format(fembloc, "02d")])

orgdicts = dict_filter (orgdicts, or_dnf =femb_cs, and_flg=False  ) 
#orgdicts = dict_del_chn (orgdicts, del_chn = [0, 0,  48]  ) 
#orgdicts = dict_del_chn (orgdicts, del_chn = [0, 0,  1]  ) 
fp = sum_path + fn + "femb%d"%loc + ".pdf" 
pp = PdfPages(fp)
print "start...wait a few minutes..."
plot0_overall_enc (pp, orgdicts, title="APA ENC vs. Tp", calitype="fpg_gain", sfhf = "hf" ) 
plot3_overall_gain (pp, orgdicts, title="APA Gain Measurement" ) 

plot2_peds (pp, orgdicts,title="Pedestals", gs=[ "140"], tp="20"  , loc = loc) 
plot1_chns_enc_1 (pp, orgdicts, title="APA ENC Distribution",  cali_cs="fpg_gain", rms_cs = "rms", gs=[ "140"], tp="05", loc=loc )  #
plot1_chns_enc_1 (pp, orgdicts, title="APA ENC Distribution",  cali_cs="fpg_gain", rms_cs = "rms", gs=[ "140"], tp="10", loc=loc )  #
plot1_chns_enc_1 (pp, orgdicts, title="APA ENC Distribution",  cali_cs="fpg_gain", rms_cs = "rms", gs=[ "140"], tp="20", loc=loc )  #
plot1_chns_enc_1 (pp, orgdicts, title="APA ENC Distribution",  cali_cs="fpg_gain", rms_cs = "rms", gs=[ "140"], tp="30", loc=loc )  #
plot4_chns_gain (pp, orgdicts, title="Gain Distribution",  g="140" , fembs_on_apa = fembs_on_apa)  #

pp.close()

print fp 
print "Done"

