# -*- coding: utf-8 -*-
"""
File Name: Main.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 1/13/2018 3:05:03 PM
Last modified: 3/13/2020 2:42:31 AM
"""

#defaut setting for scientific caculation
#import numpy
#import scipy
#from numpy import *
#import numpy as np
#import scipy as sp
#import pylab as pl

import os
import sys
import copy
from datetime import datetime
import numpy as np
import time
import pickle
from timeit import default_timer as timer

###############################################################################
from ce_runs import CE_RUNS
ceruns = CE_RUNS()

start = timer()
ceruns.APA = sys.argv[1]
ceruns.femb_meas.APA = ceruns.APA 
ceruns.env = ""
test_runs = int(sys.argv[2],16)
#RTD_flg = (sys.argv[3] == "True")
RTD_flg = False
jumbo_flag = (sys.argv[3] == "True")
phase_set = int(sys.argv[4])
if (ceruns.APA == "Anode_PCB"):
    print (ceruns.APA)
    ceruns.wib_version_id = 0x121
    ceruns.femb_ver_id = 0x501
    ceruns.path = "C:/Anode_PCB/Rawdata/" 
    ceruns.wib_ips = [  "192.168.121.1"  ]
    ceruns.wib_pwr_femb = [[1,0,0,0],]
    ceruns.femb_mask    = [[0,0,0,0]]
    ceruns.bbwib_ips = [ "192.168.121.1"] 
    ceruns.tmp_wib_ips = ["192.168.121.1"] 
    ceruns.avg_wib_ips = ["192.168.121.1"] 
    ceruns.avg_wib_pwr_femb = [[1,1,1,1]]
    ceruns.avg_femb_on_wib = [0] 
    ceruns.jumbo_flag = jumbo_flag
    ceruns.COTSADC = True
    ceruns.femb_meas.femb_config.phase_set = phase_set

ceruns.jumbo_flag_set( )
if (os.path.exists(ceruns.path)):
    pass
else:
    try: 
        os.makedirs(ceruns.path)
    except OSError:
        print ("Can't create a folder, exit")
        sys.exit()

datafp = "./data_path.txt"
logfile = ceruns.path +  ceruns.APA + "_readme.log"
monlogfile = ceruns.path +  ceruns.APA + "_monitor.log"
chk_path = "Void"
rms_path = "Void"
fpg_path = "Void"
asic_path = "Void"

if (True ):
    print ("WIEC self check")
    print ("time cost = %.3f seconds"%(timer()-start))
    ceruns.WIB_self_chk()

if (test_runs == 0x0 ):
    print ("Power FEMBs ON")
    print ("time cost = %.3f seconds"%(timer()-start))

    ceruns.FEMBs_PWR_SW(SW = "ON")
    with open(logfile, "a+") as f:
        f.write( "Begin\n") 
        f.write( "Turn PS on\n" ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )

        wib_wrerr_cnt = ceruns.femb_meas.femb_config.femb.wib_wrerr_cnt
        wib_wr_cnt = ceruns.femb_meas.femb_config.femb.wib_wr_cnt
        femb_wrerr_cnt = ceruns.femb_meas.femb_config.femb.femb_wrerr_cnt
        femb_wr_cnt = ceruns.femb_meas.femb_config.femb.femb_wr_cnt
        udp_timeout_cnt = ceruns.femb_meas.femb_config.femb.udp_timeout_cnt
        udp_hstimeout_cnt = ceruns.femb_meas.femb_config.femb.udp_hstimeout_cnt
        f.write ("There are %d times WIB UDP Registers Write\n"%wib_wr_cnt )
        f.write ("There are %d times WIB UDP Registers Write Error\n"%wib_wrerr_cnt )
        f.write ("There are %d times FEMB UDP Registers Write\n"%femb_wr_cnt )
        f.write ("There are %d times FEMB UDP Registers Write Error\n"%femb_wrerr_cnt )
        f.write ("There are %d times UDP timeouts\n"%udp_timeout_cnt )
        f.write ("There are %d times UDP High Speed links timeouts\n"%udp_hstimeout_cnt )
        udp_err_np = ceruns.udp_err_np
        for oneerr in udp_err_np:
            if (oneerr[4] - oneerr[3] != 0) : 
                f.write ("RUNcode(%s)WIB%d(%s)FEMB%d: UDP Reg Write Error count = (%d-%d) = %d\n" \
                        %(oneerr[5], oneerr[1], oneerr[0], oneerr[2], oneerr[4], oneerr[3], oneerr[3] - oneerr[4] ))
        femb_wrerr_log = ceruns.femb_meas.femb_config.femb.femb_wrerr_log
        if len(femb_wrerr_log) != 0 :
            f.write ("Write ERROR happens at FEMB%d, Addr=%x, Value=%x"%(femb_wrerr_log[0], femb_wrerr_log[1],femb_wrerr_log[2]) )
            for logn in range(len(femb_wrerr_log)-1):
                log0 = femb_wrerr_log[logn]
                log1 = femb_wrerr_log[logn+1]
                if log0 != log1 :
                    f.write ("Write ERROR happens at FEMB%d, Addr=%x, Value=%x"%(log1[0], log1[1],log1[2]) )
        for onelinkcur in ceruns.linkcurs:
            f.write( onelinkcur + "\n") 
        f.write( "End\n") 
        f.write( "\n") 

if (test_runs != 0x100 ):
    print ("FEMBs self-check")
    mask_femb = ceruns.FEMBs_Self_CHK()
    print (ceruns.COTSADC)

    with open(logfile, "a+") as f:
        f.write( "Begin\n") 
        f.write( "Broken FEMBs are masked\n" ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )
        f.write ("ADC Phase: " + str(ceruns.femb_meas.femb_config.phase_set) + "\n" )
        for onemaskfemb in mask_femb:
            f.write (onemaskfemb + "\n" )
        f.write( "End\n") 
        f.write( "\n") 

if (test_runs&0x7F != 0x0 ):
    if (False):
        print ("Please write a sentence to describe the test purpose: ")
        #test_note = raw_input("Please input: ")
    else:
        test_note = "Continuate test..."
    rtd_temp = " "
    rundate =  datetime.now().strftime('%m_%d_%Y')
    runtime =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(logfile, "a+") as f:
        f.write( "Begin\n") 
        f.write(runtime + "\n") 
        f.write(ceruns.APA + "\n") 
        f.write(ceruns.env + "\n") 
        f.write("Test Code = 0X" + format(test_runs,"02X")+ "\n")  
        f.write(test_note + "\n") 
        f.write("RTDs: %s"%rtd_temp + "\n")  
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )

    print ("FEMB ADC offset calibration")
    print ("time cost = %.3f seconds"%(timer()-start))

    if (test_runs&0x7F == 0x40):
        #oft_file = "./APA_ADC_OFT_06202018_121405.bin"
        oft_file = "./APA_ADC_OFT_06272018_222333.bin"
        with open (oft_file, 'rb') as fp:
            apa_oft_info = pickle.load(fp)
    else:
        apa_oft_info = ceruns.oft_run( ) 

    with open(logfile, "a+") as f:
        f.write( "FEMB ADC offset calibration\n" ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )

if (test_runs&0x10 != 0x0 ):
    print "Quick Checkout Test"
    print "time cost = %.3f seconds"%(timer()-start)
    chk_path = ceruns.qc_run(apa_oft_info, sgs=[1], tps =[3], val = 100) 
    with open(logfile, "a+") as f:
        f.write( "%2X: Quick Checkout Test\n" %(test_runs&0x10) ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )

if (test_runs&0x01 != 0x0 ):
    print "Noise Measurement Test"
    print "time cost = %.3f seconds"%(timer()-start)
    rms_path = ceruns.rms_run(apa_oft_info, sgs = [1], tps =[0,1,2,3], val=1600) 
    with open(logfile, "a+") as f:
        f.write( "%2X: Noise Measurement Test\n" %(test_runs&0x01) ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )

if (test_runs&0x02 != 0x0 ):
    print "FPGA DAC Calibration Test"
    print "time cost = %.3f seconds"%(timer()-start)
    fpg_path = ceruns.fpgadac_run(apa_oft_info, sgs = [1], tps =[0,1,2,3], val=100)
    with open(logfile, "a+") as f:
        f.write( "%2X: FPGA DAC Calibration Test\n" %(test_runs&0x02) ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )

if (test_runs&0x04 != 0x0 ):
    print "ASIC DAC Calibration Test"
    print "time cost = %.3f seconds"%(timer()-start)
    asic_path = ceruns.asicdac_run(apa_oft_info, sgs = [1], tps =[0,1,2,3], val=100)
    with open(logfile, "a+") as f:
        f.write( "%2X: ASIC DAC Calibration Test\n" %(test_runs&0x04) ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )

if (test_runs&0x20 != 0x0 ):
    print "Software Trigger mode"
    print "time cost = %.3f seconds"%(timer()-start)
    chk_path = ceruns.soft_triger_run(apa_oft_info, sgs=[1], tps=[3] )
    with open(logfile, "a+") as f:
        f.write( "%2X: Quick Checkout Test\n" %(test_runs&0x20) ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )

if (test_runs&0x20 != 0x0 ):
    print "Hardware Trigger mode"
    print "time cost = %.3f seconds"%(timer()-start)
    chk_path = ceruns.soft_triger_run(apa_oft_info, sgs=[1], tps=[3] )
    with open(logfile, "a+") as f:
        f.write( "%2X: Quick Checkout Test\n" %(test_runs&0x20) ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )


if (test_runs&0x80 != 0x0 ):
    print "Turn FEMBs OFF"
    print "time cost = %.3f seconds"%(timer()-start)
    ceruns.FEMBs_PWR_SW(SW = "OFF")
    with open(logfile, "a+") as f:
        f.write( "Begin\n") 
        f.write( "Turn PS OFF\n" ) 
        f.write (ceruns.runpath + "\n" )
        f.write (ceruns.runtime + "\n" )
        f.write ("Alive FEMBs: " + str(ceruns.alive_fembs) + "\n" )
        f.write( "End\n") 
        f.write( "\n") 

if (test_runs&0x7F != 0x0 ):
    if (test_runs&0x17 !=0) : 
        with open(datafp, "w+") as f:
            f.write(chk_path + "\n")
            f.write(rms_path + "\n")
            f.write(fpg_path + "\n")
            f.write(asic_path + "\n")

    with open(logfile, "a+") as f:
        wib_wrerr_cnt = ceruns.femb_meas.femb_config.femb.wib_wrerr_cnt
        wib_wr_cnt = ceruns.femb_meas.femb_config.femb.wib_wr_cnt
        femb_wrerr_cnt = ceruns.femb_meas.femb_config.femb.femb_wrerr_cnt
        femb_wr_cnt = ceruns.femb_meas.femb_config.femb.femb_wr_cnt
        udp_timeout_cnt = ceruns.femb_meas.femb_config.femb.udp_timeout_cnt
        udp_hstimeout_cnt = ceruns.femb_meas.femb_config.femb.udp_hstimeout_cnt
        f.write ("There are %d times WIB UDP Registers Write\n"%wib_wr_cnt )
        f.write ("There are %d times WIB UDP Registers Write Error\n"%wib_wrerr_cnt )
        f.write ("There are %d times FEMB UDP Registers Write\n"%femb_wr_cnt )
        f.write ("There are %d times FEMB UDP Registers Write Error\n"%femb_wrerr_cnt )
        f.write ("There are %d times UDP timeouts\n"%udp_timeout_cnt )
        f.write ("There are %d times UDP High Speed links timeouts\n"%udp_hstimeout_cnt )
        udp_err_np = ceruns.udp_err_np
        for oneerr in udp_err_np:
            if (oneerr[4] - oneerr[3] != 0) : 
                f.write ("RUNcode(%s)WIB%d(%s)FEMB%d: UDP Reg Write Error count = (%d-%d) = %d\n" \
                        %(oneerr[5], oneerr[1], oneerr[0], oneerr[2], oneerr[4], oneerr[3], oneerr[3] - oneerr[4] ))

        femb_wrerr_log = ceruns.femb_meas.femb_config.femb.femb_wrerr_log
        if len(femb_wrerr_log) != 0 :
            f.write ("Write ERROR happens at FEMB%d, Addr=%x, Value=%x\n"%(femb_wrerr_log[0][0], femb_wrerr_log[0][1],femb_wrerr_log[0][2]) )
            for logn in range(len(femb_wrerr_log)-1):
                log0 = femb_wrerr_log[logn]
                log1 = femb_wrerr_log[logn+1]
                if log0 != log1 :
                    f.write ("Write ERROR happens at FEMB%d, Addr=%x, Value=%x\n"%(log1[0], log1[1],log1[2]) )
        f.write( "End\n") 
        f.write( "\n") 

print "Well Done"


